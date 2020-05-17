from datetime import timedelta
from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase
from django.utils.timezone import now
from freezegun import freeze_time
from model_mommy import mommy

from kl_conferences.bbb_api import BBBServerUnreachable
from kl_conferences.models import Room


class TestGroupsViewSet(TestCase):
    region = 'region'

    def _groups_url(self, group):
        return f'/api/v1/groups/{group.id}/'

    def _make_server(self, **kwargs):
        fields = dict(region=self.region, cpu_count=2, load_5m=0.1)
        fields.update(kwargs)
        return mommy.make('kl_conferences.ServerNode', **fields)

    @freeze_time('2020-01-15 00:00:00')
    @mock.patch('kl_conferences.lesson_bridging_service.BigBlueButtonAPI')
    def test_start_lesson_server_unreachable_disconnected_fallback_to_valid(self, bbb_api_mock):
        # Servers, one is really dead
        server_1 = self._make_server(hostname='srv1', display_name='dsrv1', last_heartbeat=now() - timedelta(seconds=100), load_5m=1)
        server_2 = self._make_server(hostname='srv2', display_name='dsrv2', last_heartbeat=now() - timedelta(seconds=100), region='other', load_5m=1)

        # Mock API behavior
        redir_url = 'redirect.url'
        bbb_api_mock.return_value = MagicMock()
        bbb_api_mock.return_value.get_join_url.return_value = redir_url
        bbb_api_mock.return_value.create_room.side_effect = [
            # srv1 gets matched first because it's same region
            BBBServerUnreachable(hostname='srv1'),
            MagicMock(attendeePW='attendeePW', moderatorPW='moderatorPW'),
        ]

        # Mods groups, auth
        g = mommy.make('kl_participants.Group', region=self.region, display_name='grupa')
        m = mommy.make('kl_participants.Moderator')
        m.groups.add(g)
        user = m.user
        user.set_password('pass')
        user.save()
        self.client.login(username=user.username, password='pass')

        resp = self.client.post(f'{self._groups_url(g)}start_lesson/', json={})
        resp_data = resp.json()

        # Check resp
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp_data['redirect'], redir_url)

        # Check room was created
        created_room = Room.objects.filter(group=g, moderator_secret='moderatorPW', attendee_secret='attendeePW').last()
        self.assertIsNotNone(created_room)
        self.assertEquals(created_room.server_node, server_2)

        # Check servers status updated
        server_1.refresh_from_db()
        server_2.refresh_from_db()
        self.assertFalse(server_1.enabled)
        self.assertTrue(server_2.enabled)
