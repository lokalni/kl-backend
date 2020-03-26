import bigbluebutton_api_python
import socket

class BigBlueButtonAPI:
    API_URL_TEMPLATE = 'https://{hostname}/bigbluebutton/'

    def __init__(self, hostname, api_secret):
        self.api = bigbluebutton_api_python.BigBlueButton(
                self.API_URL_TEMPLATE.format(
                    hostname = hostname
                ),
                api_secret
            )

    def check_connection(self):
        try:
            # Set socket timeout globally, we could not wait more than 15s.
            socket.setdefaulttimeout(15)
            self.api.get_meetings()
            return True
        except (bigbluebutton_api_python.exception.bbbexception.BBBException,IOError):
            return False
