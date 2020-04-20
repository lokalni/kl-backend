from django.conf import settings
from django.core.exceptions import SuspiciousOperation


class BounceBotsUA:
    """Bounce broken url resolver bots."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_ua = request.headers.get('user-agent', '').lower()
        for pattern, msg in settings.BOUNCE_BOTS_UA_PATTERNS:
            if pattern.lower() in request_ua:
                raise SuspiciousOperation(msg)

        return self.get_response(request)
