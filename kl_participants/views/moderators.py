from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.conf import settings

from kl_participants.models import Moderator


def quick_login(request, token):
    mod = Moderator.objects.get(access_token=token.upper())
    login(request, mod.user)
    return HttpResponseRedirect(redirect_to=settings.DJ_LOGIN_REDIRECT)
