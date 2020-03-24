from django.db import models


class ServerNode(models.Model):
    display_name = models.CharField(max_length=255)
    url = models.CharField(max_length=1024)

    class Meta:
        db_table = 'server_nodes'

    @classmethod
    def assign_server(cls, conference):
        # TODO - assignment logic (prometheus was mentioned)
        return cls.objects.last()
