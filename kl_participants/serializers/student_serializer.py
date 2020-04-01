from rest_framework import serializers

from kl_participants.models import Student


class StudentSerializer(serializers.ModelSerializer):
    access_url = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = '__all__'

