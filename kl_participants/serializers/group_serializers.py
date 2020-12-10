from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers

from kl_conferences.models import ServerNode, PreferredServer
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
    preferred_servers = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'display_name', 'slug', 'region', 'students_count', 'preferred_servers')

    def get_slug(self, instance):
        return '{}-{}'.format(slugify(instance.display_name), str(instance.id))

    def get_preferred_servers(self, instance):
        return ServerNodeSerializer(instance.preferred_servers.order_by('-preferredserver__priority'), many=True).data

    @transaction.atomic()
    def create(self, validated_data):
        current_user_mod = self.context['request'].user.moderator
        new_group = super(GroupSerializer, self).create(validated_data)
        current_user_mod.groups.add(new_group)
        return new_group

    @transaction.atomic()
    def update(self, instance, validated_data):
        updated_group = super(GroupSerializer, self).update(instance, validated_data)
        self._handle_preferred_servers(updated_group, self.initial_data['preferred_servers'])
        return updated_group

    def _handle_preferred_servers(self, group, preferred_servers_list):
        group.preferred_servers.set([])
        group.preferred_servers.through.objects.bulk_create([
            PreferredServer(
                group_id=group.id,
                server_id=srv["id"],
                priority=len(preferred_servers_list) - idx,
            ) for (idx, srv) in enumerate(preferred_servers_list)
        ])


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
