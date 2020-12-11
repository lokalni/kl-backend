from django.contrib import admin
from django.db import models

from kl_backend.regions import Region


class Group(models.Model):
    """Studying groups"""
    display_name = models.CharField(max_length=255)
    region = models.CharField(choices=Region.choices(), max_length=32)  # TODO - move to table or convert to int id
    preferred_servers = models.ManyToManyField('kl_conferences.ServerNode', through='kl_conferences.PreferredServer')
    # TODO - add school info?

    class Meta:
        db_table = 'groups'

    def last_meeting_room(self):
        return self.room_set.last()


admin.site.register(Group)
