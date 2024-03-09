from rest_framework.exceptions import ValidationError


def validate_termii_response(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if not 200 <= response.status_code < 400:
            raise ValidationError(f"Termii SMS Sender failed with error code: {response.status_code}")

        return response.json()

    return wrapper


def remove_plus_prefix(phone_number: str) -> str:
    """Validator that removes any + prefix from a string parameter."""
    return phone_number.lstrip("+")
