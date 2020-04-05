from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    moderator_id = serializers.IntegerField(read_only=True, source='moderator_set.last.id')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'moderator_id']
