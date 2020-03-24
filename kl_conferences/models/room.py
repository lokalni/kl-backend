from django.db import models


class Room(models.Model):
    server_node = models.ForeignKey('kl_conferences.ServerNode', on_delete=models.CASCADE)
    group = models.ForeignKey('kl_participants.Group', on_delete=models.CASCADE)

    # TODO getters or cached field, capacity, participants number

    class Meta:
        db_table = 'rooms'

