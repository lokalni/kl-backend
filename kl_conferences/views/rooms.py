import logging

from django.http import HttpResponseRedirect
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action

from kl_conferences.lesson_bridging_service import get_student_access_url
from kl_conferences.models.room import Room
from kl_conferences.serializers.room_serializer import RoomSerializer


logger = logging.getLogger()


def limbo_url(token):
    return f'{settings.DOMAIN}/#/limbo/?token={token}'


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('-id')
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'], url_path='join/(?P<token>[^/]+)/?', permission_classes=[])
    def join(self, request, token):
        redirect_url = get_student_access_url(token)
        if redirect_url:
            return HttpResponseRedirect(redirect_to=redirect_url)

        return HttpResponseRedirect(redirect_to=limbo_url(token))
