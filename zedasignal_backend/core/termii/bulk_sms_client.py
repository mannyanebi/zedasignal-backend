import requests
from django.conf import settings
from requests import Response

from zedasignal_backend.core.termii.utils import clean_phone_numbers, validate_termii_response


class TermiiBulkSmsClient:
    """
    A client for termii sms services that sends sms to multiple recipients.
    Ensure recipients numbers don't begin with a + sign
    """

    def __init__(self) -> None:
        self.api_key = settings.TERMII_API_KEY
        self.from_sender = settings.TERMII_SENDER_ID
        self.channel = "dnd"
        self.type = "plain"
        self.sms_url = f"{settings.TERMII_BASE_URL}/api/sms/send/bulk"
        self.headers = {"Content-Type": "application/json"}

    @validate_termii_response
    def post(self, to: list[str], message: str, *args, **kwargs) -> Response:
        cleaned_numbers = clean_phone_numbers(to)
        payload = {
            "to": cleaned_numbers,
            "from": self.from_sender,
            "sms": message,
            "channel": self.channel,
            "type": self.type,
            "api_key": self.api_key,  # Include the API key in the query parameters
        }
        return requests.post(url=self.sms_url, json=payload, headers=self.headers)
