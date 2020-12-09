from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers

from kl_conferences.serializers.server_node_serializer import ServerNodeSerializer
from kl_participants.models import Group, Student, Moderator


class DelimitedStringsListField(serializers.CharField):
    max_length = 1024
    delimiter = '\n'
    trim_whitespace = True
    allow_blank = False

    def to_internal_value(self, data):
        strings = [s.strip() for s in data.split('\n')]
        return strings


class GroupSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.IntegerField(source='student_set.count', read_only=True)
    preferred_servers = ServerNodeSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'

    def get_slug(self, instance):
        return '{}-{}'.format(slugify(instance.display_name), str(instance.id))

    @transaction.atomic()
    def create(self, validated_data):
        current_user_mod = self.context['request'].user.moderator
        new_group = super(GroupSerializer, self).create(validated_data)
        current_user_mod.groups.add(new_group)
        return new_group


class CreateGroupFullRequestSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(min_length=2, max_length=64, write_only=True)
    delimited_participants = DelimitedStringsListField(write_only=True)

    def create(self, validated_data):
        participants = validated_data.pop('delimited_participants')

        group = super(CreateGroupFullRequestSerializer, self).create(validated_data)
        for name in participants:
            Student.create_new(group, name)

        return group

    class Meta:
        model = Group
        fields = ('display_name', 'delimited_participants')
