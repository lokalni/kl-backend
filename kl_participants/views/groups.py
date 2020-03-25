from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from kl_conferences.models import ServerNode
from kl_conferences.models.room import Room
from kl_participants.models import Group
from kl_participants.serializers.group_serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    # FIXME
    permission_classes = []

    # TODO - trim results to assigned groups
    @action(detail=True, methods=["post"])
    def create_lesson(self, request, pk):
        group = self.get_object()
        server = ServerNode.assign_server(group)
        room, _ = Room.objects.get_or_create(server_node=server, group=group)

        # TODO - Fire actual logic, create service???
        return Response(data={
            'room': {
                'id': room.id,
            },
            'assigned_server': {
                'name': server.display_name,
                'url': server.url,
            }
        })

    # TODO - add more actions on resource?
