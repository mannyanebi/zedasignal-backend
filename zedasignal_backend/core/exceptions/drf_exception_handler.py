from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler

from zedasignal_backend.core.utils.transform_errors import (
    transform_dict_errors,
    transform_error_details,
)

from ..error_response import DEFAULT_ERROR_CODES, ErrorResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        errors = generate_custom_errors_list(response.data, exc)
        return ErrorResponse(status=response.status_code, errors=errors)
    return response


def generate_custom_errors_list(data, exc):
    if isinstance(data, list):
        errors = transform_error_data_list(DEFAULT_ERROR_CODES, data)
    elif isinstance(data, dict):
        errors = transform_error_data_dict(DEFAULT_ERROR_CODES, data)
    else:
        errors = [
            {
                "code": DEFAULT_ERROR_CODES.get(400, ""),
                "message": "Something went wrong",
                "details": exc,
            }
        ]
    return errors


def transform_error_data_list(DEFAULT_ERROR_CODES, data: list):
    errors = []
    for error in data:
        if isinstance(error, ErrorDetail):
            errors.append(
                {
                    "code": DEFAULT_ERROR_CODES.get(400, ""),
                    "message": error.code,
                    "details": str(error),
                }
            )
        elif isinstance(error, list):
            errors.extend(transform_error_details(DEFAULT_ERROR_CODES, "error", error))
        elif isinstance(error, dict):
            errors.extend(transform_dict_errors(DEFAULT_ERROR_CODES, error))
        else:
            errors.append(
                {
                    "code": DEFAULT_ERROR_CODES.get(400, ""),
                    "message": str(error),
                    "details": str(error),
                }
            )
    return errors


def transform_error_data_dict(DEFAULT_ERROR_CODES, data: dict):
    errors = []
    for key, error in data.items():
        if isinstance(error, ErrorDetail):
            errors.append(
                {
                    "code": DEFAULT_ERROR_CODES.get(400, ""),
                    "message": error.code,
                    "details": str(error),
                }
            )
        elif isinstance(error, list):
            errors.extend(transform_error_details(DEFAULT_ERROR_CODES, key, error))
        elif isinstance(error, dict):
            errors.extend(transform_dict_errors(DEFAULT_ERROR_CODES, error))
        else:
            errors.append(
                {
                    "code": DEFAULT_ERROR_CODES.get(400, ""),
                    "message": f"{key} - {str(error)}",
                    "details": str(error),
                }
            )
    return errors
