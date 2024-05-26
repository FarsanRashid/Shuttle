import json
from typing import cast

from redis import Redis

from accounts.models import Passenger
from domain.model import PendingOtpValidation
from service_layer.exceptions import InvalidPayload, VerificationFailed
from utils.attributes import (
    error_incorrect_otp,
    error_invalid_json,
    error_invalid_token,
    error_missing_field,
)


def validate_payload(payload):
    if not all(payload):
        raise InvalidPayload(error_missing_field)

    if not all(isinstance(value, str)
               for value in payload):
        raise InvalidPayload(error_invalid_json)


def validate_signup(token: str, otp: str, cache: Redis):
    validate_payload((token, otp))

    value = cast(str, cache.get(token))
    if value is None:
        raise VerificationFailed(error_invalid_token)

    pending_otp_validation = PendingOtpValidation(
        **json.loads(value))

    if pending_otp_validation.OTP != otp:
        raise VerificationFailed(error_incorrect_otp)

    Passenger.objects.create_user(
        username=pending_otp_validation.username,
        password=pending_otp_validation.password).save()
