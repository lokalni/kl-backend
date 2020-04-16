import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from kl_backend.regions import Region
from kl_conferences.models import ServerNode


class ServerNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServerNode
        fields = '__all__'


class HostnameField(serializers.CharField):
    max_length = 128

    def to_internal_value(self, data):
        data = str(data)
        if not re.match(r'^([\w\d]+\.)+\w+(:\d+)?$', data):
            raise ValidationError('Incorrect hostname format!')
        return data


class ServerNodeRegisterRequestSerializer(serializers.Serializer):
    hostname = HostnameField()
    api_secret = serializers.CharField(max_length=64)  # here_goes_bbb_api_secret


class ServerNodeHeartBeatRequestSerializer(serializers.Serializer):
    cpu_count = serializers.IntegerField(min_value=0, max_value=256)
    load_5m = serializers.DecimalField(min_value=0, decimal_places=2, max_digits=6)
    api_secret = serializers.CharField(max_length=64)  # here_goes_bbb_api_secret
    hostname = HostnameField()
    region = serializers.ChoiceField(choices=Region.choices())
