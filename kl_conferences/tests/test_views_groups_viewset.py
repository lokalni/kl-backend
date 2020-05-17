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

    def _two_servers_region_priority_setup(self):
        # higher prio, same region
        server_1 = self._make_server(
            hostname='srv1', display_name='dsrv1', last_heartbeat=now() - timedelta(seconds=100), load_5m=1)
        server_2 = self._make_server(
            hostname='srv2', display_name='dsrv2', last_heartbeat=now() - timedelta(seconds=100), region='other', load_5m=1)

        g = mommy.make('kl_participants.Group', region=self.region, display_name='grupa')
        m = mommy.make('kl_participants.Moderator')
        m.groups.add(g)
        user = m.user
        user.set_password('pass')
        user.save()

        return server_1, server_2, g, user

    @freeze_time('2020-01-15 00:00:00')
    @mock.patch('kl_conferences.lesson_bridging_service.BigBlueButtonAPI')
    def test_start_lesson_server_unreachable_disconnected_fallback_to_valid(self, bbb_api_mock):
        server_1, server_2, group, user = self._two_servers_region_priority_setup()
        # Mock API behavior
        redir_url = 'redirect.url'
        bbb_api_mock.return_value = MagicMock()
        bbb_api_mock.return_value.get_join_url.return_value = redir_url
        bbb_api_mock.return_value.create_room.side_effect = [
            # srv1 gets matched first because it's same region
            BBBServerUnreachable(hostname='srv1'),
            MagicMock(attendeePW='attendeePW', moderatorPW='moderatorPW'),
        ]

        self.client.login(username=user.username, password='pass')
        resp = self.client.post(f'{self._groups_url(group)}start_lesson/', json={})
        resp_data = resp.json()

        # Check resp
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp_data['redirect'], redir_url)

        # Check room was created
        self.assertTrue(Room.objects.filter(
            server_node=server_2,
            group=group,
            moderator_secret='moderatorPW',
            attendee_secret='attendeePW'
        ).exists())

        # Check servers status updated
        server_1.refresh_from_db()
        server_2.refresh_from_db()
        self.assertFalse(server_1.enabled)
        self.assertTrue(server_2.enabled)

    @freeze_time('2020-01-15 00:00:00')
    @mock.patch('kl_conferences.lesson_bridging_service.BigBlueButtonAPI')
    def test_start_lesson_server_unreachable_room_exists(self, bbb_api_mock):
        """
        When server is unreachable and room exists, previous room should be purged,
        server disconnected from pool and different server used.
        """
        server_1, server_2, group, user = self._two_servers_region_priority_setup()
        # Create existing room - server will be unreachable
        room = mommy.make('kl_conferences.Room', group=group, server_node=server_1)

        # Mock BBB API
        def mock_is_meeting_running(meeting_id):
            if meeting_id == room.bbb_meeting_id:
                return False
            raise NotImplementedError("Outdated test")

        def mock_create_room(meeting_id, *args, **kwargs):
            for_server = Room.objects.get(id=meeting_id).server_node
            if for_server== server_1:
                raise BBBServerUnreachable(hostname=for_server.hostname)
            else:
                return MagicMock(attendeePW='attendeePW', moderatorPW='moderatorPW')

        redir_url = 'redirect.url'

        mocked_api = MagicMock()
        mocked_api.is_meeting_running.side_effect = mock_is_meeting_running
        mocked_api.get_join_url.return_value = redir_url
        mocked_api.create_room.side_effect = mock_create_room
        bbb_api_mock.return_value = mocked_api

        # Request
        self.client.login(username=user.username, password='pass')
        resp = self.client.post(f'{self._groups_url(group)}start_lesson/', json={})
        resp_data = resp.json()

        # Check resp
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp_data['redirect'], redir_url)

        # Check room was created
        self.assertTrue(Room.objects.filter(
            server_node=server_2,
            group=group,
            moderator_secret='moderatorPW',
            attendee_secret='attendeePW'
        ).exists())

        # Check previous room purged
        self.assertFalse(Room.objects.filter(id=room.id).exists())

        # Check servers status updated
        server_1.refresh_from_db()
        server_2.refresh_from_db()
        self.assertFalse(server_1.enabled)
        self.assertTrue(server_2.enabled)