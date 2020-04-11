import collections
import hashlib
from urllib.parse import urlencode
from collections import OrderedDict
import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from xml.etree import ElementTree

from logging import getLogger

logger = getLogger()

RET_CODE_FAILED = 'FAILED'
RET_CODE_SUCCESS = 'SUCCESS'
API_URL_TEMPLATE = 'https://{hostname}/bigbluebutton/api/{method}'


def apibool(boolean): return {True: 'true', False: 'false'}[boolean]


class BBBRequestFailed(Exception):
    pass


class RoomAlreadyExistsError(BBBRequestFailed):
    pass


BBBRoom = collections.namedtuple('BBBRoom',
                                 'meetingID internalMeetingID parentMeetingID attendeePW moderatorPW createTime '
                                 'voiceBridge dialNumber createDate hasUserJoined duration hasBeenForciblyEnded '
                                 'returncode messageKey message'
                                 )


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
        assert hostname and api_secret, 'Api client requires hostname and password!'

        self.hostname = hostname
        self.api_secret = api_secret


    def _build_url(self, method, **qs_params):
        base_url = API_URL_TEMPLATE.format(
            hostname=self.hostname,
            method=method,
        )
        qs = urlencode(OrderedDict(**qs_params)) if qs_params else ''
        checksum = self._calc_checksum(method, qs)
        qs = qs + '&' if qs else ''
        return f'{base_url}?{qs}checksum={checksum}'

    def _get(self, method, **qs_params):
        full_url = self._build_url(method, **qs_params)

        logger.info(f'Calling BBB API GET {full_url}')
        resp = requests.get(full_url, timeout=15)
        logger.debug(f'Received: {resp.status_code} {resp.content}')

        if resp.status_code != 200:
            raise BBBRequestFailed(f'Invalid response status: {resp.status_code}')

        return ElementTree.fromstring(resp.content)

    def _calc_checksum(self, method, querystring):
        blob = method + querystring + self.api_secret
        logger.debug(f"Creating checksum from {blob}")
        return hashlib.sha1(blob.encode('utf-8')).hexdigest()

    def _assert_resp_success(self, xml_resp):
        if xml_resp.find('returncode').text != RET_CODE_SUCCESS:
            resp_content = ElementTree.tostring(xml_resp)
            raise BBBRequestFailed(f'Request failed: {resp_content}')

    def get_meetings(self):
        """
        Fetch meetings list
        http://yourserver.com/bigbluebutton/api/getMeetings?checksum=[checksum]
        :return:
        """
        # TODO - return meetings
        xml_resp = self._get('getMeetings')
        self._assert_resp_success(xml_resp)
        return []

    def is_meeting_running(self, meeting_id: str):
        """Check if given meeting is running."""
        xml_resp = self._get('isMeetingRunning', meetingID=meeting_id)
        self._assert_resp_success(xml_resp)
        return xml_resp.find('running').text == 'true'

    def check_connection(self):
        """Validate can establish connection with server."""
        try:
            self.get_meetings()
        except (ConnectionError, ConnectTimeout, BBBRequestFailed):
            return False

        return True

    def create_room(self, meeting_id: str, attendee_secret: str, moderator_secret: str,
                    max_participants: int = 50, guestPolicy: str = 'ALWAYS_ACCEPT', webcam_mod_only: bool = True):
        """
        Creates room in BBB server
        https://docs.bigbluebutton.org/dev/api.html#create

        API Call returns

        <response>
          <returncode>SUCCESS</returncode>
          <meetingID>Test</meetingID>
          <internalMeetingID>640ab2bae07bedc4c163f679a746f7ab7fb5d1fa-1531155809613</internalMeetingID>
          <parentMeetingID>bbb-none</parentMeetingID>
          <attendeePW>ap</attendeePW>
          <moderatorPW>mp</moderatorPW>
          <createTime>1531155809613</createTime>
          <voiceBridge>70757</voiceBridge>
          <dialNumber>613-555-1234</dialNumber>
          <createDate>Mon Jul 09 17:03:29 UTC 2018</createDate>
          <hasUserJoined>false</hasUserJoined>
          <duration>0</duration>
          <hasBeenForciblyEnded>false</hasBeenForciblyEnded>
          <messageKey>duplicateWarning</messageKey>
          <message>This conference was already in existence and may currently be in progress.</message>
        </response>

        :returns BBBRoom
        """
        xml_resp = self._get('create', **{
            'meetingID': meeting_id,
            'attendeePW:': attendee_secret,
            'moderatorPW': moderator_secret,
            # 'dialNumber': no setup yet
            # 'voiceBridge': no setup yet
            'maxParticipants': max_participants,
            # 'logoutURL': no need for now
            'record': apibool(False),
            # 'duration: no need for now
            # 'meta_*': no need for now
            # 'moderatorOnlyMessage': no need for now
            'webcamsOnlyForModerator': apibool(webcam_mod_only),
            # 'logo':
            # 'bannerText':
            # 'copyright':
            'muteOnStart': apibool(True),
            'lockSettingsDisablePrivateChat': apibool(True),
            'lockSettingsDisablePublicChat': apibool(False),
            'lockSettingsDisableNote': apibool(False),
            # 'lockSettingsLockedLayout': no idea
            'guestPolicy': guestPolicy,  # ALWAYS_ACCEPT, ALWAYS_DENY
        })
        if xml_resp.find('messageKey').text == 'idNotUnique':
            raise RoomAlreadyExistsError
        self._assert_resp_success(xml_resp)

        return BBBRoom(**{child.tag: child.text for child in xml_resp})

    def get_join_url(self, meeting_id: str, password: str, join_as: str, assing_user_id: str,
             join_via_html5: bool = False, user_is_guest: bool = False):
        """
        Builds url allowing user to join the meeting.
        When user is redirected to that url he'll automatically join the room.

        https://docs.bigbluebutton.org/dev/api.html#join
        :returns url for redirect
        """
        return self._build_url('join', **{
            'meetingID': meeting_id,
            'password': password,
            'fullName': join_as,
            'userID': assing_user_id,
            'joinViaHtml5': apibool(join_via_html5),
            'guest': apibool(user_is_guest),
            'redirect': apibool(True),
        })
