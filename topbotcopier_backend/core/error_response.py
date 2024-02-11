# noqa: E501

from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from zedasignal_backend.core.utils.transform_errors import (
    handle_and_validate_errors_list,
    validate_and_transform_errors,
)

DEFAULT_ERROR_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    402: "PAYMENT_REQUIRED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    406: "NOT_ACCEPTABLE",
    407: "PROXY_AUTHENTICATION_REQUIRED",
    408: "REQUEST_TIMEOUT",
    409: "CONFLICT",
    410: "GONE",
    411: "LENGTH_REQUIRED",
    412: "PRECONDITION_FAILED",
    413: "PAYLOAD_TOO_LARGE",
    414: "URI_TOO_LONG",
    415: "UNSUPPORTED_MEDIA_TYPE",
    416: "RANGE_NOT_SATISFIABLE",
    417: "EXPECTATION_FAILED",
    418: "I'M_A_TEAPOT",
    429: "TOO_MANY_REQUESTS",
    500: "INTERNAL_SERVER_ERROR",
    501: "NOT_IMPLEMENTED",
    502: "BAD_GATEWAY",
    503: "SERVICE_UNAVAILABLE",
    504: "GATEWAY_TIMEOUT",
    505: "HTTP_VERSION_NOT_SUPPORTED",
}

# You can associate these error codes with the default error messages for your API's error responses.

ErrorDict = dict[str, str]

DEFAULT_ERROR_MESSAGES = {
    400: "Bad request. The request parameters are invalid.",
    401: "Unauthorized. Authentication is required to access this resource.",
    402: "Payment required. Payment is needed to access this resource.",
    403: "Forbidden. You don't have permission to access this resource.",
    404: "Not found. The requested resource does not exist.",
    405: "Method not allowed. The HTTP method is not allowed for this resource.",
    406: "Not acceptable. The requested resource can't produce the desired content.",
    407: "Proxy authentication required. Authentication with a proxy server is required.",
    408: "Request timeout. The server timed out waiting for the request.",
    409: "Conflict. There's a conflict with the current state of the resource.",
    410: "Gone. The requested resource has been permanently removed.",
    411: "Length required. The 'Content-Length' header is missing in the request.",
    412: "Precondition failed. A precondition in the request header failed.",
    413: "Payload too large. The request payload is too large.",
    414: "URI too long. The request URI is too long.",
    415: "Unsupported media type. The request's media type is not supported.",
    416: "Range not satisfiable. The requested range is not valid for the resource.",
    417: "Expectation failed. An expectation specified in the request header can't be met.",
    418: "I'm a teapot. This server refuses to brew coffee because it is, in fact, a teapot.",
    429: "Too many requests. You have exceeded the rate limit for this resource.",
    500: "Internal server error. An unexpected server error occurred.",
    501: "Not implemented. The server does not support the functionality required.",
    502: "Bad gateway. The server received an invalid response from an upstream server.",
    503: "Service unavailable. The server is currently unable to handle the request.",
    504: "Gateway timeout. The server timed out waiting for an upstream server's response.",
    505: "HTTP version not supported. The server does not support the HTTP protocol version used in the request.",
}


# You can use these messages in your error responses as needed.
class ErrorResponse(Response):
    def __init__(
        self,
        status: int,
        message: str | None = None,
        details: list[str] | str | ReturnDict | None = None,
        errors: list[ErrorDict] | None = None,
    ):
        """
        This class is used to create error responses for your API.
        If you want to return as list of errors, pass the errors argument as a list.
        Otherwise, pass the error response using the arguments status, message, and details.

        Args:
            status (int): HTTP status code for the error response.
            message (str | None, optional): Error message based on HTTP status,
            you can pass custom message. Defaults to None.
            details (list[str] | str | ReturnDict | None, optional): Error description or
            further details. Defaults to None.
            errors (list[ErrorDict] | None, optional):  List of errors, more than one,
            ensure the follow response structure as in ErrorResponseChildSerializer. Defaults to None.
        """

        error_data = self.generate_error_data(status, message, details, errors)
        super().__init__(data=error_data, status=status)

    def generate_error_data(
        self,
        status: int,
        message: str | None,
        details: list[str] | str | ReturnDict | None,
        errors: list[ErrorDict] | None,
    ):
        serializer_errors_as_list = self.validate_and_transform_serializer_errors(
            details
        )
        errors_as_list = handle_and_validate_errors_list(errors)

        if serializer_errors_as_list is not None:
            errors_as_list = (
                (errors_as_list + serializer_errors_as_list)
                if errors_as_list is not None
                else serializer_errors_as_list
            )

        error_data = {
            "success": False,
            "error": self.generate_error_item(status, message, details, errors_as_list),
        }
        return error_data

    def generate_error_item(self, status, message, details, errors_as_list):
        if errors_as_list is None:
            return [
                {
                    "code": DEFAULT_ERROR_CODES.get(status, ""),
                    "message": message or DEFAULT_ERROR_MESSAGES.get(status, ""),
                    "details": details or "",
                }
            ]
        return errors_as_list

    def validate_and_transform_serializer_errors(
        self, details: list[str] | str | None | ReturnDict = None
    ) -> list[ErrorDict] | None:
        serializer_errors = validate_and_transform_errors(
            DEFAULT_ERROR_CODES, details=details
        )
        if isinstance(serializer_errors, list) and len(serializer_errors) > 0:
            return handle_and_validate_errors_list(serializer_errors)
