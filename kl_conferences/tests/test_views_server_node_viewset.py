from unittest import mock

from django.test import TestCase
from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse

from kl_backend.regions import Region
from kl_conferences.models import ServerNode


class TestServerNodeSelfServiceViewset(TestCase):
    valid_keepalive_pars = dict(load_5m=1, cpu_count=2, api_secret='secret',
                                hostname='serwer.lokalni.pl', region=Region.LUBELSKIE)

    nodes_url = '/api/v1/nodes/'

    @mock.patch('kl_conferences.models.server_node.BigBlueButtonAPI.check_connection')
    def test_register_ok(self, check_connection):
        check_connection.return_value = True
        domain = 'serwer.lokalni.pl'
        resp = self.client.post(self.nodes_url, data={'hostname': domain, 'api_secret': 'secret'}, format='json')

        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        check_connection.assert_called()
        self.assertTrue(ServerNode.objects.filter(hostname=domain, api_secret='secret'))

    @mock.patch('kl_conferences.models.server_node.BigBlueButtonAPI.check_connection')
    def test_register_while_existing_updates(self, check_connection):
        check_connection.return_value = True
        domain = 'serwer.lokalni.pl'
        server = mommy.make('kl_conferences.ServerNode', hostname=domain, api_secret='old_secret')

        resp = self.client.post(self.nodes_url, data={'hostname': domain, 'api_secret': 'new_secret'}, format='json')
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        check_connection.assert_called()
        server.refresh_from_db()
        self.assertEquals(server.hostname, domain)
        self.assertEquals(server.api_secret, 'new_secret')

    @mock.patch('kl_conferences.models.server_node.BigBlueButtonAPI.check_connection')
    def test_register_fail_no_connection_not_confirmed(self, check_connection):
        check_connection.return_value = False
        domain = 'serwer.lokalni.pl'

        resp = self.client.post(self.nodes_url, data={'hostname': domain, 'api_secret': 'secret'}, format='json')
        self.assertEquals(resp.status_code, status.HTTP_304_NOT_MODIFIED)
        check_connection.assert_called()
        self.assertEquals(ServerNode.objects.count(), 0)

    @mock.patch('kl_conferences.models.server_node.BigBlueButtonAPI.check_connection')
    def test_register_fail_domain_mismatch(self, check_connection):
        check_connection.return_value = True
        domain = 'serwer.lokalni.com.pl'

        resp = self.client.post(self.nodes_url, data={'hostname': domain, 'api_secret': 'secret'}, format='json')
        self.assertEquals(resp.status_code, status.HTTP_304_NOT_MODIFIED)
        check_connection.assert_not_called()
        self.assertEquals(ServerNode.objects.count(), 0)

    def test_keepalive_existing(self):
        server = mommy.make('kl_conferences.ServerNode', hostname=self.valid_keepalive_pars['hostname'],
                            api_secret=self.valid_keepalive_pars['api_secret'])
        resp = self.client.post(f'{self.nodes_url}keepalive/', data=self.valid_keepalive_pars, format='json')

        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        server.refresh_from_db()
        self.assertEquals(server.load_5m, self.valid_keepalive_pars['load_5m'])
        self.assertEquals(server.cpu_count, self.valid_keepalive_pars['cpu_count'])
        self.assertEquals(server.region, self.valid_keepalive_pars['region'])

    def test_keepalive_non_existing_or_invalid_pass(self):
        server = mommy.make('kl_conferences.ServerNode', hostname='invalid.lokalni.pl',
                            api_secret=self.valid_keepalive_pars['api_secret'])
        resp = self.client.post(f'{self.nodes_url}keepalive/', data=self.valid_keepalive_pars, format='json')

        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)
        server.refresh_from_db()
        self.assertNotEqual(server.load_5m, self.valid_keepalive_pars['load_5m'])
        self.assertNotEqual(server.cpu_count, self.valid_keepalive_pars['cpu_count'])
        self.assertNotEqual(server.region, self.valid_keepalive_pars['region'])

