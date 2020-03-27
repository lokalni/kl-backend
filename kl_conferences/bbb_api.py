import hashlib
from urllib.parse import urlencode
from collections import OrderedDict
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from xml.etree import ElementTree

from logging import getLogger


logger = getLogger()

RET_CODE_FAILED = 'FAILED'
API_URL_TEMPLATE = 'https://{hostname}/bigbluebutton/api/{method}'


def apibool(boolean): return {True: 'true', False: 'false'}[boolean]


class BigBlueButtonAPI:
    """
    https://docs.bigbluebutton.org/dev/api.html#api-security-model

    Failure resp:

    <response>
      <returncode>FAILED</returncode>
      <messageKey>checksumError</messageKey>
      <message>You did not pass the checksum security check</message>
    </response>'

    """
    def __init__(self, hostname, api_secret):
        assert hostname and api_secret

        self.hostname = hostname
        self.api_secret = api_secret

    def _get(self, method, **qs_params):
        base_url = API_URL_TEMPLATE.format(
            hostname=self.hostname,
            method=method,
        )
        qs = urlencode(OrderedDict(**qs_params)) + '&' if qs_params else ''
        checksum = self._calc_checksum(method, qs)
        full_url = f'{base_url}?{qs}checksum={checksum}'

        logger.info(f'Calling BBB API GET {full_url}')
        resp = requests.get(full_url, timeout=15)
        logger.debug(f'Received: {resp.status_code} {resp.content}')

        assert resp.status_code == 200
        tree = ElementTree.fromstring(resp.content)
        assert tree.find('returncode').text != RET_CODE_FAILED

        return tree

    def _calc_checksum(self, method, querystring):
        blob = method+querystring+self.api_secret
        logger.debug(f"Creating checksum from {blob}")
        return hashlib.sha1(blob.encode('utf-8')).hexdigest()

    def get_meetings(self):
        """
        Fetch meetings list
        http://yourserver.com/bigbluebutton/api/getMeetings?checksum=[checksum]
        :return:
        """
        # TODO - return meetings
        xml_tree = self._get('getMeetings')
        return []

    def is_meeting_running(self, meeting_id: str):
        """Check if given meeting is running."""
        xml_tree = self._get('isMeetingRunning', meetingID=meeting_id)
        return xml_tree.find('running').text == 'true'

    def check_connection(self):
        """Validate can establish connection with server."""
        try:
            self.get_meetings()
        except (ConnectionError, ConnectTimeout, AssertionError):
            return False

        return True

    def join(self, meeting_id: str, password: str, join_as: str, assing_user_id: str,
             join_via_html5: bool = False, user_is_guest: bool = False):
        """Sends join request, returns url for redirecting user to."""
        xml_tree = self._get('join', **{
            'meetingID': meeting_id,
            'password': password,
            'fullName': join_as,
            'userID': assing_user_id,
            'joinViaHtml5': apibool(join_via_html5),
            'guest': apibool(user_is_guest),
            'redirect': apibool(False),  # TODO - not sure here
        })
        return xml_tree.find('url').text
