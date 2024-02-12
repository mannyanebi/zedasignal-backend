from rest_framework import serializers, status
from rest_framework.response import Response

DEFAULT_SUCCESS_MESSAGES = {
    200: "Resource fetched successfully.",
    201: "Resource created successfully.",
    202: "Resource updated successfully.",
    203: "Response contains non-authoritative information.",
    204: "Resource deleted successfully.",
    205: "Data reset to its initial state.",
    206: "Partial content retrieved successfully.",
    207: "Multiple operations completed successfully.",
    208: "Resource already reported and no further action required.",
    226: "Informational response with representation used.",
}


class SuccessResponse(Response):
    def __init__(
        self,
        *,
        status: int = status.HTTP_200_OK,
        message: str | None = None,
        data=None,
    ):
        success_data = {
            "success": True,
            "message": message if message is not None else DEFAULT_SUCCESS_MESSAGES.get(status, ""),
            "result": data if data is not None else {},
        }
        super().__init__(data=success_data, status=status)


class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
    success = serializers.BooleanField(default=True)
    result = serializers.DictField(child=serializers.CharField(), allow_empty=True, read_only=True)
