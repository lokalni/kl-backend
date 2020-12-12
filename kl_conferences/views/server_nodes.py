from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from kl_conferences.models import ServerNode
from kl_conferences.serializers.server_node_serializer import (
    ServerNodeRegisterRequestSerializer,
    ServerNodeHeartBeatRequestSerializer,
    ServerNodeSerializer)


class ServerNodeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ServerNodeSerializer
    queryset = ServerNode.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['region']
    search_fields = ['hostname', 'display_name']


class ServerNodeSelfServiceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ServerNodeRegisterRequestSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        node = ServerNode.register_server_node(**serializer.data)
        return Response(status=status.HTTP_200_OK if node is not None else status.HTTP_304_NOT_MODIFIED)

    @action(detail=False, methods=['post'], serializer_class=ServerNodeHeartBeatRequestSerializer)
    def keepalive(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ServerNode.record_heartbeat(**serializer.data)
        except ServerNode.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response()
