import logging
from datetime import timedelta
from decimal import Decimal as D

from django.contrib import admin
from django.db import models
from django.db.models import F, ExpressionWrapper, DecimalField, Value, IntegerField
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from django.conf import settings

from kl_backend.regions import Region
from kl_conferences.bbb_api import BigBlueButtonAPI

logger = logging.getLogger()


class ServerNode(models.Model):
    display_name = models.CharField(max_length=255, unique=True)
    hostname = models.CharField(max_length=1024, unique=True)
    api_secret = models.CharField(max_length=64)
    enabled = models.BooleanField(default=True)
    region = models.CharField(choices=Region.choices(), max_length=32,
                              null=True)  # TODO - move to table or convert to int ids
    cpu_count = models.SmallIntegerField(null=True)
    load_5m = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    last_heartbeat = models.DateTimeField(null=True)
    last_assigned = models.DateTimeField(null=True)

    class ServerNodeManager(models.Manager):

        @property
        def active(self):
            """Available for assignments."""
            return self.get_queryset().filter(
                last_heartbeat__gt=now() - timedelta(seconds=settings.MAX_HEARTBEAT_DELAY),
                load_5m__isnull=False,
                enabled=True,
            )

    objects = ServerNodeManager()

    class Meta:
        db_table = 'server_nodes'

    def __repr__(self):
        return f'<{self.__class__.__name__}: id[{self.id}] hostname[{self.hostname}]>'

    @classmethod
    def assign_server(cls, group):
        """Choose best server to host lesson for given group."""
        max_delay = settings.MAX_HEARTBEAT_DELAY
        max_load = settings.MAX_SAME_REGION_LOAD_PER_CPU

        node_candidates = cls.objects.active.annotate(
            load_per_cpu=ExpressionWrapper(
                F('load_5m') / F('cpu_count'),
                output_field=DecimalField()
            ),
            priority=Value(0, IntegerField()),
        ).filter(load_per_cpu__lt=max_load)

        # Check valid preferred servers exist
        preferred_servers_candidates = node_candidates.filter(preferredserver__group=group)
        if preferred_servers_candidates.exists():
            node_candidates = preferred_servers_candidates.annotate(
                priority=Coalesce('preferredserver__priority', 0),
            )

        def node_weight(n):
            """Evaluates preferred server, region and load"""
            last_assigned = n.last_assigned or now() - timedelta(seconds=max_delay)
            la_v = D((now() - last_assigned).seconds) / D(max_delay)
            la_w = D('0.3')
            cpu_v = n.load_per_cpu
            cpu_w = 1 - la_w
            return (
                n.priority,
                n.region == group.region,
                la_v * la_w - cpu_v * cpu_w,
            )

        node_candidates = sorted(node_candidates, key=node_weight, reverse=True)
        try:
            server = node_candidates[0]
        except IndexError:
            logger.error(f'No server available for {group.id} {group.display_name}!')
            raise ServerNode.DoesNotExist

        # Get it further from load balancer
        server.last_assigned = now()
        server.save()

        logger.info(f'Group {group.id} {group.display_name} assigned server {server.hostname}')
        return server

    @classmethod
    def record_heartbeat(cls, hostname, api_secret, **update_kwargs):
        server = ServerNode.objects.get(hostname=hostname, api_secret=api_secret)
        server.last_heartbeat = now()
        for k, v in update_kwargs.items():
            setattr(server, k, v)
        server.save()
        return server

    @classmethod
    def register_server_node(cls, hostname, api_secret, display_name=None):
        # Verify hostname from allowed domain
        if not hostname.endswith(settings.BBB_DOMAIN_ALLOWED):
            return

        api = BigBlueButtonAPI(hostname, api_secret)
        if api.check_connection():
            try:
                server_node = ServerNode.objects.get(hostname=hostname)
            except ServerNode.DoesNotExist:
                server_node = ServerNode(hostname=hostname, display_name=display_name or hostname)

            server_node.api_secret = api_secret
            server_node.save()

            return server_node

    def disconnect_from_pool(self):
        """Temporarily disable server until next heartbeat."""
        self.enabled = False
        self.save()


admin.site.register(ServerNode)
