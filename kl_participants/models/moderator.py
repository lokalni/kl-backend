import uuid

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from kl_backend.utils import get_token


class Moderator(models.Model):
    """Teachers can start lessons and manage rooms."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ManyToManyField('kl_participants.Group')
    display_name = models.CharField(max_length=255)
    access_token = models.CharField(max_length=8, unique=True, default=get_token)

    class Meta:
        db_table = 'moderators'

    @property
    def uuid(self):
        return f'moderator:{self.id}'

    @property
    def access_url(self):
        return f'{settings.DOMAIN}/l/{self.access_token}'


admin.site.register(Moderator)
