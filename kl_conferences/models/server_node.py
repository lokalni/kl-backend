import logging
from datetime import timedelta
from decimal import Decimal as D

from django.contrib import admin
from django.db import models
from django.db.models import F, ExpressionWrapper, DecimalField
from django.utils.timezone import now
from django.conf import settings

from kl_backend.regions import Region
from kl_conferences.bbb_api import BigBlueButtonAPI


logger = logging.getLogger()


class ServerNode(models.Model):
    display_name = models.CharField(max_length=255, unique=True)
    hostname = models.CharField(max_length=1024, unique=True)
    api_secret = models.CharField(max_length=64)
    # Metrics delivered with heartbeat, all null at creation
    region = models.CharField(choices=Region.choices(), max_length=32, null=True)  # TODO - move to table or convert to int ids
    cpu_count = models.SmallIntegerField(null=True)
    load_5m = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    last_heartbeat = models.DateTimeField(null=True)
    last_assigned = models.DateTimeField(null=True)

    MAX_HEARTBEAT_DELAY = 5 * 60  # seconds
    MAX_SAME_REGION_LOAD_PER_CPU = D('0.82137')

    class Meta:
        db_table = 'server_nodes'

    @classmethod
    def assign_server(cls, group):
        """Choose best server to host lesson for given group."""
        node_candidates = cls.objects.filter(
            last_heartbeat__gt=now() - timedelta(seconds=cls.MAX_HEARTBEAT_DELAY)
        ).annotate(load_per_cpu=ExpressionWrapper(F('load_5m')/F('cpu_count'), output_field=DecimalField()))
        same_region_low_load = node_candidates.filter(
            region=group.region,
            load_per_cpu__lt=cls.MAX_SAME_REGION_LOAD_PER_CPU
        )
        # print([same_region_low_load[0].load_per_cpu, same_region_low_load[0].load_5m, same_region_low_load[0].cpu_count])
        if same_region_low_load.exists():
            node_candidates = same_region_low_load

        def node_weight(n):
            last_assigned = n.last_assigned or now() - timedelta(seconds=cls.MAX_HEARTBEAT_DELAY)
            la_v = D((now() - last_assigned).seconds) / D(cls.MAX_HEARTBEAT_DELAY)
            la_w = D('0.3')
            cpu_v = n.load_per_cpu
            cpu_w = 1 - la_w
            return la_v * la_w - cpu_v * cpu_w

        node_candidates = sorted(node_candidates, key=node_weight)
        try:
            server = node_candidates[0]
        except IndexError:
            logger.error(f'No server available for {group.id} {group.display_name}!')
            return None

        logger.info(f'Group {group.id} {group.display_name} assigned server {server.hostname}')
        return server

    @classmethod
    def record_heartbeat(cls, hostname, api_secret, **update_kwargs):
        server = ServerNode.objects.get(hostname=hostname, api_secret=api_secret)
        server.last_heartbeat = now(),
        for k, v in update_kwargs.items():
            setattr(server, k, v)
        server.save()

    @classmethod
    def register_server_node(cls, hostname, api_secret, display_name=None):
        # Verify hostname from allowed domain
        if not hostname.endswith(settings.BBB_DOMAIN_ALLOWED):
            return

        api = BigBlueButtonAPI(hostname, api_secret)
        if api.check_connection():
            server_node, _ = ServerNode.objects.update_or_create(
                display_name=display_name or hostname,
                hostname=hostname,
                defaults={'api_secret': api_secret},
            )
            return server_node


admin.site.register(ServerNode)
