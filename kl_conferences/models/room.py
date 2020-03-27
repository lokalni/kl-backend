from django.contrib import admin
from django.db import models


class Room(models.Model):
    server_node = models.ForeignKey('kl_conferences.ServerNode', on_delete=models.CASCADE)
    group = models.ForeignKey('kl_participants.Group', on_delete=models.CASCADE)
    attendee_secret = models.CharField(max_length=64, null=True)
    moderator_secret = models.CharField(max_length=64, null=True)

    class Meta:
        db_table = 'rooms'

    @property
    def bbb_meeting_id(self):
        return str(self.id)


admin.site.register(Room)
