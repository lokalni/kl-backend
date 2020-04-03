from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from kl_conferences.models import ServerNode
from kl_conferences.serializers.server_node_serializer import (
    ServerNodeRegisterRequestSerializer,
    ServerNodeHeartBeatRequestSerializer,
)


class ServerNodeSelfServiceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ServerNodeRegisterRequestSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node = ServerNode.register_server_node(**serializer.data)
        return Response(status=status.HTTP_200_OK if node is not None else status.HTTP_304_NOT_MODIFIED)

    @action(detail=False, methods=['post'], serializer_class=ServerNodeHeartBeatRequestSerializer, permission_classes=[])
    def keepalive(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ServerNode.record_heartbeat(**serializer.data)
        except ServerNode.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response()
