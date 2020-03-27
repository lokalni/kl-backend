from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.serializers import Serializer

from kl_conferences.lesson_bridging_service import start_lesson
from kl_participants.models import Group, Moderator
from kl_participants.serializers.group_serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    # FIXME
    permission_classes = []

    # TODO - trim results to assigned groups
    @action(detail=True, methods=["post"], serializer_class=Serializer)
    def start_lesson(self, request, pk):
        """Create and join as moderator."""
        group = self.get_object()
        # TODO - get moderator from user
        moderator = group.moderator_set.last()

        try:
            redirect_url = start_lesson(group, moderator)
        except Exception as e:
            # TODO - something smarter?
            raise APIException(str(e))

        return HttpResponseRedirect(redirect_to=redirect_url)
