from django.db import models


class Group(models.Model):
    """Studying groups"""
    display_name = models.CharField(max_length=255)
    # TODO - add school info?

    class Meta:
        db_table = 'groups'
