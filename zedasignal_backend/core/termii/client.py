import requests
from django.conf import settings
from requests import Response

from zedasignal_backend.core.termii.utils import remove_plus_prefix, validate_termii_response


class TermiiClient:
    """
    A client for termii sms services
    """

    def __init__(self) -> None:
        self.api_key = settings.TERMII_API_KEY
        self.from_sender = settings.TERMII_SENDER_ID
        self.channel = "dnd"
        self.type = "plain"
        self.sms_url = f"{settings.TERMII_BASE_URL}/api/sms/send"
        self.headers = {"Content-Type": "application/json"}

    @validate_termii_response
    def post(self, to: str, message: str, *args, **kwargs) -> Response:
        params = {
            "to": remove_plus_prefix(to),
            "from": self.from_sender,
            "sms": message,
            "channel": self.channel,
            "type": self.type,
            "api_key": self.api_key,  # Include the API key in the query parameters
        }
        return requests.post(url=self.sms_url, params=params, headers=self.headers)
