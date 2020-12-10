from django.db import models


class PreferredServer(models.Model):
    """
    Link between group and server for selection algorithm lookup priority.
    """
    server = models.ForeignKey('kl_conferences.ServerNode', on_delete=models.CASCADE)
    group = models.ForeignKey('kl_participants.Group', on_delete=models.CASCADE)
    priority = models.SmallIntegerField()

    class Meta:
        unique_together = ('server', 'group')
        ordering = ('id',)