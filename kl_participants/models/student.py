from django.db import models, transaction
from django.conf import settings

from kl_backend.utils import get_token


class Student(models.Model):
    """Students participate in conference rooms created by teachers."""
    group = models.ForeignKey('kl_participants.Group', on_delete=models.PROTECT)
    display_name = models.CharField(max_length=255)
    access_token = models.CharField(max_length=8, unique=True, default=get_token)

    class Meta:
        db_table = 'students'

    @property
    def uuid(self):
        # TODO Save uuid in table, use py module short uuid propose by @consi
        return f'student:{self.id}'

    @property
    def access_url(self):
        return f'{settings.DOMAIN}/{self.access_token}'

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
        self.access_token = get_token();
