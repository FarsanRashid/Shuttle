import json
import random
from typing import Any

from django.conf import settings
import jwt
import redis

from accounts.models import Passenger
from domain.model import PendingOtpValidation
from service_layer.exceptions import InvalidPayload, UserNameNotUnique
from utils.attributes import USERNAME, error_invalid_payload
from utils.config import SIGNUP_OTP_TTL
from utils.otp_sender import get_sms_sender


def validate_payload(username, password, country_dial_code, contact_number):
    payload: tuple[Any, ...] = (
        username, password, country_dial_code, contact_number)
    if not all(isinstance(value, str)
               for value in payload):
        raise InvalidPayload(error_invalid_payload)

    if len(country_dial_code.strip()) < 1 or len(contact_number.strip()) < 1:
        raise InvalidPayload(error_invalid_payload)


def initate_signup(username, password, country_dial_code, contact_number, cache: redis.Redis):

    validate_payload(username, password, country_dial_code, contact_number)

    if Passenger.objects.filter(username=username).exists():
        raise UserNameNotUnique

    jwt_token = jwt.encode(
        {USERNAME: username, }, settings.SECRET_KEY)

    otp = str(random.randint(1000, 9999))
    pending_otp_validation = PendingOtpValidation(username,
                                                  password, otp, country_dial_code.strip(),
                                                  contact_number.strip())

    if cache.set(jwt_token,
                 json.dumps(pending_otp_validation._asdict()), nx=True,
                 ex=SIGNUP_OTP_TTL):
        try:
            otp_sender = get_sms_sender(pending_otp_validation.country_code)
            otp_sender.send(pending_otp_validation.contact_number, otp)
        except Exception as e:
            cache.delete(jwt_token)
            raise e
        return jwt_token
    raise UserNameNotUnique
