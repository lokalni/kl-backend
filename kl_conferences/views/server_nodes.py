from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from kl_conferences.models import ServerNode
from kl_conferences.serializers.server_node_serializer import (
    ServerNodeRegisterRequestSerializer,
    ServerNodeHeartBeatRequestSerializer,
)


class ServerNodeSelfServiceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return ServerNodeRegisterRequestSerializer
        elif self.action == 'keepalive':
            return ServerNodeHeartBeatRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ServerNode.register_server_node(**serializer.data)
        return Response()

    @action(detail=False, methods=['post'])
    def keepalive(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ServerNode.record_heartbeat(**serializer.data)
        return Response()
