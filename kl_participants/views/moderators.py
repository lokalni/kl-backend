from django.contrib.auth import login
from django.http import HttpResponseRedirect
from rest_framework import viewsets, permissions

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
