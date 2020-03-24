from django.db import models


class Student(models.Model):
    """Students participate in conference rooms created by teachers."""
    group = models.ForeignKey('kl_participants.Group', on_delete=models.PROTECT)
    display_name = models.CharField(max_length=255)
    access_token = models.CharField(max_length=8)

    class Meta:
        db_table = 'students'
