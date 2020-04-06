from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from kl_participants.models import Moderator


class ModeratorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    display_name = serializers.CharField(max_length=255)

    @transaction.atomic()
    def create(self, validated_data):
        email = validated_data['user']['email']
        validated_data['user'] = User.objects.create(username=email, email=email, is_staff=False)
        return super(ModeratorSerializer, self).create(validated_data)

    class Meta:
        model = Moderator
        fields = ['id', 'email', 'display_name', 'access_url']
