import json
from typing import cast

from accounts.models import Passenger
from adapters.cache import AbstractCache
from domain.model import PendingOtpValidation
from service_layer.exceptions import InvalidPayload, VerificationFailed
from utils.attributes import (
    error_incorrect_otp,
    error_invalid_payload,
    error_invalid_token,
)


def validate_payload(payload):
    if not all(payload):
        raise InvalidPayload(error_invalid_payload)

    if not all(isinstance(value, str)
               for value in payload):
        raise InvalidPayload(error_invalid_payload)


def validate_signup(token: str, otp: str, cache: AbstractCache):
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
        password=pending_otp_validation.password,
        contact_number=pending_otp_validation.contact_number,
        country_code=pending_otp_validation.country_code).save()
    cache.delete(token)
