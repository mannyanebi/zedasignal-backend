import string
from typing import TypedDict

import phonenumbers
import requests
from django.conf import settings
from django.utils.crypto import get_random_string


def generate_numeric_code(length=6):
    """
    Generate a random 6 digit string of numbers.
    We use this formatting to allow leading 0s.
    """
    return get_random_string(length, allowed_chars=string.digits)


def add_count(data: dict | list, count: int) -> dict:
    return dict(data=data, count=count)


class SmsParams(TypedDict):
    username: str
    from_: str
    to: str
    message: str


def send_sms_using_proxy_server(params: SmsParams):
    """
    Send SMS using SMS2Email API

    Args:
        params (SmsParams): The parameters to be sent to the API

    Returns:
        response: HTTP Response
    """

    url = settings.SMS2EMAILAPI_URL
    payload = {
        "username": params["username"],
        "from": params["from_"],
        "to": params["to"],
        "message": params["message"],
    }
    # Send the GET request
    response = requests.get(url, params=payload)

    return response


def normalize_phone_number(value):
    try:
        # Parse the input value as a phone number
        phone_number = phonenumbers.parse(value, None)

        # Check if the number is valid
        if not phonenumbers.is_valid_number(phone_number):
            raise ValueError("Invalid phone number")

        # Normalize the number to E.164 format
        normalized_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

        return normalized_number
    except phonenumbers.phonenumberutil.NumberParseException as phone_number_parse_error:
        raise ValueError(str(phone_number_parse_error))
