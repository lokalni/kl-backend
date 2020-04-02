from django.db import transaction
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from kl_conferences.lesson_bridging_service import start_lesson
from kl_conferences.models import ServerNode
from kl_participants.models import Group
from kl_participants.serializers.group_serializers import GroupSerializer, CreateGroupFullRequestSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer

    # TODO - trim results to assigned groups
    @action(detail=True, methods=["post"], serializer_class=Serializer)
    def start_lesson(self, request, pk):
        """Create and join as moderator."""
        group = self.get_object()
        # TODO - get moderator from user
        moderator = group.moderator_set.last()

        try:
            redirect_url = start_lesson(group, moderator)
        except ServerNode.DoesNotExist as e:
            # TODO - something smarter?
            raise ParseError('Brak dostępnego serwera.')

        return Response(data={'redirect': redirect_url})

    @transaction.atomic
    @action(detail=False, methods=["post"], serializer_class=CreateGroupFullRequestSerializer)
    def create_group_full(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(GroupSerializer(instance=serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)
