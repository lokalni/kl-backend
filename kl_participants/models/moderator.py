from django.contrib import admin
from django.db import models


class Moderator(models.Model):
    """Teachers can start lessons and manage rooms."""
    groups = models.ManyToManyField('kl_participants.Group')
    display_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'moderators'

    @property
    def uuid(self):
        return f'moderator:{self.id}'


admin.site.register(Moderator)
