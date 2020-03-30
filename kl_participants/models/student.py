from django.db import models

import string
import shortuuid


class Student(models.Model):
    """Students participate in conference rooms created by teachers."""
    group = models.ForeignKey('kl_participants.Group', on_delete=models.PROTECT)
    display_name = models.CharField(max_length=255)
    access_token = models.CharField(max_length=8) # TODO - add unique or use django token addon

    TOKEN_LENGTH = 6
    TOKEN_ALPHABET = '123456789' + string.ascii_uppercase[:36].replace('O', '')

    class Meta:
        db_table = 'students'

    @property
    def uuid(self):
        # TODO Save uuid in table, use py module short uuid propose by @consi
        return f'student:{self.id}'

    @classmethod
    def create_new(cls, group, display_name):
        return Student.objects.create(
            group=group,
            display_name=display_name,
            access_token=shortuuid.ShortUUID(alphabet=cls.TOKEN_ALPHABET).random(length=cls.TOKEN_LENGTH),
        )
