from django.contrib.auth import login
from django.http import HttpResponseRedirect
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from kl_backend.utils import get_token
from kl_participants.models import Moderator
from kl_participants.serializers.moderator_serializer import ModeratorSerializer


def quick_login(request, token):
    mod = Moderator.objects.get(access_token=token.upper())
    login(request, mod.user)
    return HttpResponseRedirect(redirect_to='/')


class ModeratorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Moderator.objects.order_by('-id')
    serializer_class = ModeratorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__email', 'display_name']

    @action(detail=True, methods=["post"], serializer_class=Serializer)
    def reset_access(self, request, pk):
        """Create and join as moderator."""
        moderator = self.get_object()
        moderator.access_token = get_token()
        moderator.save()
        moderator.refresh_from_db()
        return Response(data=ModeratorSerializer(instance=moderator).data)
