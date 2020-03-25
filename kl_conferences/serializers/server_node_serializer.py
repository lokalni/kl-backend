from rest_framework import serializers

from kl_backend.regions import Region
from kl_conferences.models import ServerNode


class ServerNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServerNode
        fields = '__all__'


class ServerNodeRegisterRequestSerializer(serializers.Serializer):
    hostname = serializers.URLField()  # "http://bbb1.agooddomain.pl/",
    api_secret = serializers.CharField(max_length=64)  # here_goes_bbb_api_secret


class ServerNodeHeartBeatRequestSerializer(serializers.Serializer):
    cpu_count = serializers.IntegerField(min_value=0, max_value=32)
    load_5m = serializers.DecimalField(min_value=0, decimal_places=2, max_digits=6)
    api_secret = serializers.CharField(max_length=64)  # here_goes_bbb_api_secret
    hostname = serializers.URLField()  # "http://bbb1.agooddomain.pl/",
    region_name = serializers.ChoiceField(choices=Region.choices())
