import re

from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from kl_backend.utils import get_token
from kl_participants.models import Moderator, Group
from kl_participants.serializers.moderator_serializer import ModeratorSerializer


def quick_login(request, token):
    """
    Moderator quick login

    GET /l/TOKEN

    Optional param g might contain landing group.
    """
    mod = get_object_or_404(Moderator, access_token__iexact=token)
    login(request, mod.user)

    # Support instant group access
    try:
        group_id = int(re.findall(r'\d+$', request.GET['g'])[0])
        group = mod.groups.get(id=group_id)
        return HttpResponseRedirect(redirect_to=f'/#/groups/{group.id}/')
    except (KeyError, IndexError, ValueError, Group.DoesNotExist):
        pass

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
