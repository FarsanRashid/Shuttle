from collections import namedtuple
import json
import random

from django.conf import settings
import jwt
import redis

from accounts.models import Passenger
from utils.attributes import OTP, PASSWORD, USERNAME
from utils.otp_sender import DianaHost


class InvalidPayload(Exception):
    pass


class UserNameNotUnique(Exception):
    pass


PendingOtpValidation = namedtuple(
    'PendingOtpValidation', [USERNAME, PASSWORD, OTP])


def initate_signup(username, password, country_code, contact_number, cache: redis.Redis):
    if not username or not password or not country_code or not contact_number:
        raise InvalidPayload

    if Passenger.objects.filter(username=username).exists():
        raise UserNameNotUnique

    jwt_token = jwt.encode(
        {USERNAME: username, }, settings.SECRET_KEY)

    otp = random.randint(1000, 9999)
    pending_otp_validation = PendingOtpValidation(
        username, password, otp)

    if cache.set(jwt_token,
                 json.dumps(pending_otp_validation._asdict()), nx=True, ex=300):
        otp_sender = DianaHost()
        otp_sender.send(otp)
        return jwt_token
    raise UserNameNotUnique
