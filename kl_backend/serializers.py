from django.contrib.auth.models import User
from rest_framework import serializers


from kl_participants.serializers.moderator_serializer import ModeratorSerializer


class UserSerializer(serializers.ModelSerializer):
    moderator = ModeratorSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'moderator']
        depth = 1
