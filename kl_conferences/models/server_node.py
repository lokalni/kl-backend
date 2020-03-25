from django.contrib import admin
from django.db import models
from django.utils.timezone import now

from kl_backend.regions import Region
from kl_conferences.bbb_api import BigBlueButtonAPI


class ServerNode(models.Model):
    display_name = models.CharField(max_length=255, unique=True)
    hostname = models.CharField(max_length=1024, unique=True)
    api_secret = models.CharField(max_length=64)
    # Metrics delivered with heartbeat, all null at creation
    region = models.CharField(choices=Region.choices(), max_length=32, null=True)  # TODO - move to table or convert to int ids
    cpu_count = models.SmallIntegerField(null=True)
    load_5m = models.DecimalField(decimal_places=2, max_digits=6, null=True)
    last_heartbeat = models.DateTimeField(null=True)

    class Meta:
        db_table = 'server_nodes'

    @classmethod
    def assign_server(cls, group):
        """Choose best server to host lesson for given group."""
        # TODO - assignment logic (prometheus was mentioned)
        return cls.objects.last()

    @classmethod
    def record_heartbeat(cls, hostname, api_secret, **update_kwargs):
        server = ServerNode.objects.get(hostname=hostname, api_secret=api_secret)
        server.update(
            last_heartbeat=now(),
            **update_kwargs
        )
        server.save()

    @classmethod
    def register_server_node(cls, hostname, api_secret):
        api = BigBlueButtonAPI(hostname, api_secret)
        api.check_connection()

        return ServerNode.objects.create(
            hotname=hostname,
            api_secret=api_secret,
        )


admin.site.register(ServerNode)
