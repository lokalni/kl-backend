import uuid

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models, transaction

from kl_backend.utils import get_token


def empty_user():
    return User.objects.create(
        username=str(uuid.uuid4())
    ).id


class Moderator(models.Model):
    """Teachers can start lessons and manage rooms."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=empty_user)
    groups = models.ManyToManyField('kl_participants.Group')
    display_name = models.CharField(max_length=255)
    access_token = models.CharField(max_length=8, unique=True, default=get_token)

    class Meta:
        db_table = 'moderators'

    # @transaction.atomic()
    # def save(self, *args, **kwargs):
    #     # When saving object, create user automagically
    #     is_new = not self.pk and not self.user
    #     super(Moderator, self).save(*args, **kwargs)
    #     if is_new:
    #         self.user = User.objects.create(username=self.uuid)
    #         self.save()

    @property
    def uuid(self):
        return f'moderator:{self.id}'


admin.site.register(Moderator)
