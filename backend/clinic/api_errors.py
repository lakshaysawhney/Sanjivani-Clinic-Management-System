from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_handler


class Conflict(APIException):
    status_code = 409
    default_detail = "This slot is already occupied, or the record changed. Refresh and try again."


def exception_handler(exc, context):
    if isinstance(exc, IntegrityError):
        return Response({"detail": str(Conflict.default_detail)}, status=409)
    if isinstance(exc, DjangoValidationError):
        return Response({"detail": exc.messages}, status=400)
    return drf_handler(exc, context)
