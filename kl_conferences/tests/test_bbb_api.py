from django.test import TestCase

from kl_conferences.bbb_api import BigBlueButtonAPI, BBBServerUnreachable


class TestServerNodeTest(TestCase):

    def test_is_meeting_running_with_unreachable_server_not_rises(self):
        """Unmocked, check behavior with non-existent server."""
        api = BigBlueButtonAPI(hostname='this.hostname.is.totally.fake', api_secret='dddd')
        self.assertFalse(api.is_meeting_running('fake_meeting_id'))

    def test_check_connection_with_unreachable_server_not_rises(self):
        """Unmocked, check behavior with non-existent server."""
        api = BigBlueButtonAPI(hostname='this.hostname.is.totally.fake', api_secret='dddd')
        self.assertFalse(api.check_connection())

    def test_check_create_room_with_unreachable_server_rises(self):
        """Unmocked, check behavior with non-existent server."""
        api = BigBlueButtonAPI(hostname='this.hostname.is.totally.fake', api_secret='dddd')
        self.assertRaises(BBBServerUnreachable, api.create_room, meeting_id='abc', attendee_secret='def', moderator_secret='ghi')
