import json

from rest_framework.exceptions import APIException, ErrorDetail, ValidationError
from rest_framework.utils.serializer_helpers import ReturnDict

from zedasignal_backend.apps.users.api.serializers import ErrorResponseChildSerializer

ErrorDict = dict[str, str]


def validate_and_transform_errors(
    DEFAULT_ERROR_CODES, *, details: list[str] | str | None | ReturnDict = None
) -> list[ErrorDict] | None:
    if details is None:
        return None

    errors = []
    if isinstance(details, ReturnDict):
        errors.extend(transform_return_dict_errors(DEFAULT_ERROR_CODES, details))
    if isinstance(details, Exception):
        errors.extend(transform_exception_errors(DEFAULT_ERROR_CODES, details))
    return errors


def transform_return_dict_errors(DEFAULT_ERROR_CODES, details: ReturnDict):
    errors = []
    for key, value in details.items():
        if isinstance(value, list) and isinstance(value[0], ErrorDetail):
            errors.append(
                {
                    "code": DEFAULT_ERROR_CODES.get(400, ""),
                    "message": f"{key}: {value[0].code}",
                    "details": str(value[0]),
                }
            )
        elif isinstance(value, dict):
            errors.extend(transform_dict_errors(DEFAULT_ERROR_CODES, value))
        else:
            errors.append(
                {
                    "code": DEFAULT_ERROR_CODES.get(400, ""),
                    "message": f"{key}: {value}",
                    "details": str(value),
                }
            )
    return errors


def transform_exception_errors(DEFAULT_ERROR_CODES, details: Exception):
    errors = []
    if isinstance(details, APIException):
        if isinstance(details.detail, list):
            for error in details.detail:
                errors.append(
                    {
                        "code": DEFAULT_ERROR_CODES.get(400, ""),
                        "message": f"{error}",
                        "details": str(error),
                    }
                )
        elif isinstance(details.detail, dict):
            errors.extend(transform_dict_errors(DEFAULT_ERROR_CODES, details.detail))
        else:
            errors.append(
                {
                    "code": DEFAULT_ERROR_CODES.get(400, ""),
                    "message": f"{details}",
                    "details": str(details),
                }
            )
    else:
        errors.append(
            {
                "code": DEFAULT_ERROR_CODES.get(400, ""),
                "message": f"{details}",
                "details": str(details),
            }
        )
    return errors


def transform_dict_errors(DEFAULT_ERROR_CODES, details: dict):
    errors = []
    for key, value in details.items():
        if isinstance(value, list) and isinstance(value[0], ErrorDetail):
            errors.extend(transform_error_details(DEFAULT_ERROR_CODES, key, value))
        elif isinstance(value, dict):
            for error_key, error_value in value.items():
                errors.append(
                    {
                        "code": DEFAULT_ERROR_CODES.get(400, ""),
                        "message": f"{error_key}: {error_value}",
                        "details": str(error_value),
                    }
                )
        else:
            errors.append(
                {
                    "code": DEFAULT_ERROR_CODES.get(400, ""),
                    "message": f"{key}: {value}",
                    "details": str(value),
                }
            )
    return errors


def transform_error_details(DEFAULT_ERROR_CODES, key, value):
    return [
        {
            "code": DEFAULT_ERROR_CODES.get(400, ""),
            "message": f"{key}: {error.code}",
            "details": str(error),
        }
        for error in value
        if isinstance(error, ErrorDetail)
    ]


def handle_and_validate_errors_list(
    errors: list[ErrorDict] | None,
) -> list[ErrorDict] | None:
    if errors is None:
        return None
    if not isinstance(errors, list):
        raise ValidationError("Errors must be passed as a list")
    for error in errors:
        serializer = ErrorResponseChildSerializer(data=error)
        if not serializer.is_valid():
            raise ValidationError(
                f"Invalid error structure: {json.dumps(error, indent=4)}"
            )
    return errors
