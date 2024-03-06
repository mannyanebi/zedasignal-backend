# from functools import wraps

from rest_framework import status

from zedasignal_backend.apps.users.models import User
from zedasignal_backend.core.error_response import ErrorResponse

# def client_required():
#     """
#     Decorator for views that checks that the logged in user is a client,
#     else returns a 403 Forbidden response.
#     """

#     def view_wrapper_function(decorated_view_function):
#         """
#         This intermediate wrapper function takes the
#         decorated View function (e.g. get, post) itself.
#         """

#         @wraps(decorated_view_function)
#         def enforce_client(view, request, *args, **kwargs):
#             user = request.user
#             if user.is_client and user.is_active and user.is_verified:
#                 return decorated_view_function(view, request, *args, **kwargs)
#             else:
#                 return ErrorResponse(
#                     details="You are not authorized to access this resource",
#                     status=status.HTTP_403_FORBIDDEN,
#                 )

#         return enforce_client

#     return view_wrapper_function


def admin_required(function=None):
    """
    Decorator for views that checks that the logged in user is an admin,
    else returns a 403 Forbidden response.
    """

    user_is_admin = lambda user: user.type == User.ADMIN and user.is_active and user.is_verified  # type: ignore # noqa: E731, E501

    def _wrapped_view(self, request, *args, **kwargs):
        if user_is_admin(request.user):
            if function:
                return function(self, request, *args, **kwargs)
        else:
            return ErrorResponse(
                details="You are not authorized to access this resource",
                status=status.HTTP_403_FORBIDDEN,
            )

    if function:
        return _wrapped_view

    return user_is_admin
