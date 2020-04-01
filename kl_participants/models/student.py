from django.db import models, transaction

import string
import shortuuid


class Student(models.Model):
    """Students participate in conference rooms created by teachers."""
    group = models.ForeignKey('kl_participants.Group', on_delete=models.PROTECT)
    display_name = models.CharField(max_length=255)
    access_token = models.CharField(max_length=8, unique=True) # TODO - add unique or use django token addon

    TOKEN_LENGTH = 6
    TOKEN_ALPHABET = '123456789' + string.ascii_uppercase[:36].replace('O', '')

    class Meta:
        db_table = 'students'

    @property
    def uuid(self):
        # TODO Save uuid in table, use py module short uuid propose by @consi
        return f'student:{self.id}'

    @property
    def access_url(self):
        # TODO - use settings var for domain
        return f'tk.lokalni.pl/{self.access_token}'

    @classmethod
    @transaction.atomic
    def create_new(cls, group, display_name):
        student = Student(
            group=group,
            display_name=display_name,
        )
        student.reset_token()
        student.save()
        return student

    def reset_token(self):
        self.access_token = shortuuid.ShortUUID(alphabet=self.TOKEN_ALPHABET).random(length=self.TOKEN_LENGTH),
