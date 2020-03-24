from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from kl_conferences.models.room import Room
from kl_conferences.serializers.room_serializer import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('-id')
    serializer_class = RoomSerializer
    # FIXME
    permission_classes = []

