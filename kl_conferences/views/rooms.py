from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from kl_conferences.models.room import Room
from kl_conferences.serializers.room_serializer import RoomSerializer
from kl_participants.models import Student


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('-id')
    serializer_class = RoomSerializer
    # FIXME
    permission_classes = []

    @action(detail=False, methods=['get'], url_path='join/(?P<token>[^/]+)/?')
    def join(self, request, token):
        # TODO - do it right, get logic out of views, add permissions, add real redirect
        student = get_object_or_404(Student, access_token=token)
        lesson = get_object_or_404(Room, group=student.group)
        return Response(data=RoomSerializer(lesson).data)
