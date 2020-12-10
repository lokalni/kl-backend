from datetime import timedelta
from decimal import Decimal as D

from django.test import TestCase
from django.utils.timezone import now
from model_mommy import mommy
from freezegun import freeze_time

from kl_conferences.models import ServerNode, PreferredServer


class TestServerNodeTest(TestCase):
    def setUp(self) -> None:
        self.region = 'abc'

    def _make_server(self, **kwargs):
        fields = dict(region=self.region, cpu_count=2, load_5m=0.1)
        fields.update(kwargs)
        return mommy.make('kl_conferences.ServerNode', **fields)

    def test_server_assignment_no_servers(self):
        g = mommy.make('kl_participants.Group')
        self.assertRaises(ServerNode.DoesNotExist, ServerNode.assign_server, g)

    @freeze_time('2020-01-15 00:00:00')
    def test_excludes_dead_servers(self):
        serv1 = self._make_server(last_heartbeat=now() - timedelta(seconds=301))
        g = mommy.make('kl_participants.Group', region=self.region)
        self.assertRaises(ServerNode.DoesNotExist, ServerNode.assign_server, g)

    @freeze_time('2020-01-15 00:00:00')
    def test_server_assignemnt_disabled_server(self):
        serv1 = self._make_server(last_heartbeat=now() - timedelta(seconds=100), enabled=False)
        g = mommy.make('kl_participants.Group', region=self.region)
        self.assertRaises(ServerNode.DoesNotExist, ServerNode.assign_server, g)

    @freeze_time('2020-01-15 00:00:00')
    def test_server_assignemnt_same_region_pref(self):
        serv_local = self._make_server(last_heartbeat=now() - timedelta(seconds=100))
        serv_other = self._make_server(last_heartbeat=now() - timedelta(seconds=100), region='other')
        g = mommy.make('kl_participants.Group', region=self.region)
        self.assertEquals(ServerNode.assign_server(g), serv_local)

    @freeze_time('2020-01-15 00:00:00')
    def test_server_assignemnt_same_region_pref_respects_high_load(self):
        serv_other = self._make_server(display_name='dupa2', last_heartbeat=now() - timedelta(seconds=100), region='other', load_5m=1)
        serv_local = self._make_server(display_name='dupa', last_heartbeat=now() - timedelta(seconds=100), load_5m=1.90)
        g = mommy.make('kl_participants.Group', region=self.region)
        self.assertEquals(ServerNode.assign_server(g), serv_other)

    @freeze_time('2020-01-15 00:00:00')
    def test_server_assignemnt_pref_server_precedence(self):
        serv_local = self._make_server(last_heartbeat=now() - timedelta(seconds=100))
        serv_other_region_pref = self._make_server(last_heartbeat=now() - timedelta(seconds=100), region='other')
        g = mommy.make('kl_participants.Group', region=self.region)
        PreferredServer.objects.create(group=g, server=serv_other_region_pref, priority=1)
        self.assertEquals(ServerNode.assign_server(g), serv_other_region_pref)

    @freeze_time('2020-01-15 00:00:00')
    def test_server_assignemnt_pref_server_precedence_multiple_by_assignment_id(self):
        serv_assigned_last = self._make_server(last_heartbeat=now() - timedelta(seconds=100))
        serv_assigned_first = self._make_server(last_heartbeat=now() - timedelta(seconds=100))
        g = mommy.make('kl_participants.Group', region=self.region)
        PreferredServer.objects.create(group=g, server=serv_assigned_first, priority=2)
        PreferredServer.objects.create(group=g, server=serv_assigned_last, priority=1)
        self.assertEquals(ServerNode.assign_server(g), serv_assigned_first)

    @freeze_time('2020-01-15 00:00:00')
    def test_server_assignemnt_pref_server_precedence_respects_high_load(self):
        serv_other = self._make_server(display_name='dupa2', last_heartbeat=now() - timedelta(seconds=100), region='other', load_5m=1)
        serv_pref_high_load = self._make_server(display_name='dupa', last_heartbeat=now() - timedelta(seconds=100), load_5m=1.90)
        g = mommy.make('kl_participants.Group', region=self.region)
        PreferredServer.objects.create(group=g, server=serv_pref_high_load, priority=1)
        self.assertEquals(ServerNode.assign_server(g), serv_other)