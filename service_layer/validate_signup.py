import json

from django.conf import settings
import jwt
from redis import Redis

from service_layer.exceptions import InvalidPayload, VerificationFailed
from utils.attributes import (
    OTP,
    USERNAME,
    PASSWORD,
    error_incorrect_otp,
    error_invalid_json,
    error_invalid_token,
    error_missing_field,
)

from accounts.models import Passenger


def validate_payload(payload):
    if not all(payload):
        raise InvalidPayload(error_missing_field)

    if not all(isinstance(value, str)
               for value in payload):
        raise InvalidPayload(error_invalid_json)


def validate_signup(token: str, otp: str, cache: Redis):
    validate_payload((token, otp))

    pending_otp_validation = cache.get(token)
    if pending_otp_validation is None:
        raise VerificationFailed(error_invalid_token)

    pending_otp_validation = json.loads(pending_otp_validation)

    if pending_otp_validation.get(OTP) != otp:
        raise VerificationFailed(error_incorrect_otp)

    username = pending_otp_validation.get(USERNAME)
    password = pending_otp_validation.get(PASSWORD)

    Passenger.objects.create_user(
        username=username, password=password).save()
