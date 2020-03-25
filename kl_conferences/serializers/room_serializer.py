from rest_framework import serializers

from kl_conferences.models import Room
from kl_conferences.serializers.server_node_serializer import ServerNodeSerializer


class RoomSerializer(serializers.ModelSerializer):
    server_node = ServerNodeSerializer()

    class Meta:
        model = Room
        fields = '__all__'
