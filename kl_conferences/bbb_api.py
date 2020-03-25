import requests


class BigBlueButtonAPI:
    API_URL_TEMPLATE = 'https://{hostname}/bigbluebutton/api/{path})'

    def __init__(self, hostname, api_secret):
        self.hostname = hostname
        self.api_secret = api_secret

    def _request(self, request_method, path, **kwargs):
        url = self.API_URL_TEMPLATE.format(
            hostname=self.hostname,
            path=path,
        )
        return request_method(url, **kwargs)

    def check_connection(self):
        resp = self._request(requests.get, 'getMeetings')
        assert resp.status_code == 200
