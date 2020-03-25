from rest_framework import serializers

from kl_conferences.models import ServerNode


class ServerNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServerNode
        fields = '__all__'
