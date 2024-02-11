import base64
import string
import unicodedata
from math import asin, cos, radians, sin, sqrt
from typing import TypedDict

import phonenumbers
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from rest_framework import serializers


def generate_numeric_code(length=6):
    """
    Generate a random 6 digit string of numbers.
    We use this formatting to allow leading 0s.
    """
    return get_random_string(length, allowed_chars=string.digits)


def unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    normalized1 = unicodedata.normalize("NFKC", s1)
    normalized2 = unicodedata.normalize("NFKC", s2)

    return normalized1.casefold() == normalized2.casefold()


class CurrentClient:
    """
    This is used to get the currently logged in user,
    in this case: Client
    Similar to DRF's serializer.CurrentUserDefault class
    """

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.clients

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class CurrentTechnician:
    """
    This is used to get the currently logged in user,
    in this case: Client
    Similar to DRF's serializer.CurrentUserDefault class
    """

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.technicians

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, str):
            # Check if the base64 string is in the "data:" format
            if "data:" in data and ";base64," in data:
                # Break out the header from the base64 content
                header, data = data.split(";base64,")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            # Generate file name:
            import time

            current_date_time = time.strftime("%d/%m/%Y__%H:%M:%S", time.localtime())
            file_name = current_date_time
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = f"{file_name}.{file_extension}"

            data = ContentFile(decoded_file, name=complete_file_name)

        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class Base64FileField(serializers.FileField):
    """
    A Django REST framework field for handling file-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, str):
            # Check if the base64 string is in the "data:" format
            if "data:" in data and ";base64," in data:
                # Break out the header from the base64 content
                header, data = data.split(";base64,")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail("invalid_image")

            # Generate file name:
            import time

            current_date_time = time.strftime("%d/%m/%Y__%H:%M:%S", time.localtime())
            file_name = current_date_time
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = f"{file_name}.{file_extension}"

            data = ContentFile(decoded_file, name=complete_file_name)

        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension_mapping = {
            "jpeg": "jpg",
        }

        extension = imghdr.what(file_name, decoded_file)
        extension = extension_mapping.get(extension, extension)  # type: ignore

        return extension


def distance_between_two_points(lat1, lat2, lon1, lon2):
    """
    To calculate the distance between two points
    using their longitude and latitude

    In our case, used to calculate distances
    between clients and technicians
    """
    # converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r


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
