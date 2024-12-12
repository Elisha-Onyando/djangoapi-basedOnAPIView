from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import APIException
from rest_framework import status

class CustomIsAuthenticated(IsAuthenticated):
    # @staticmethod
    def not_authenticated(self, request, detail=None):
        # Customize the error message
        custom_message = "You must be authenticated to access this resource."
        raise NotAuthenticated(custom_message)


class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Requested resource not found"
    default_code = 'not_found'

    def __init__(self, detail=None, code=None):
        if detail:
            self.detail = detail
        elif code:
            self.code = code
        else:
            self.detail = self.default_detail