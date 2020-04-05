from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from kl_backend.serializers import UserSerializer


class AccountsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = []

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data['email']
        password = request.data['password']
        try:
            username = User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            assert user
        except (User.DoesNotExist, AssertionError):
            raise ParseError('Login failed.')

        login(request, user)
        return Response(UserSerializer(instance=user).data)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response()
