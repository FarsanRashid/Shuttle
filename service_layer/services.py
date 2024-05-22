from collections import namedtuple
import json
import random

from django.conf import settings
import jwt
import redis

from accounts.models import Passenger
from utils.otp_sender import DianaHost


class InvalidPayload(Exception):
    pass


class UserNameNotUnique(Exception):
    pass


PendingOtpValidation = namedtuple(
    'PendingOtpValidation', ['username', 'password', 'otp'])


def initate_signup(username, password, cache: redis.Redis):
    if not username or not password:
        raise InvalidPayload

    if Passenger.objects.filter(username=username).exists():
        raise UserNameNotUnique

    jwt_token = jwt.encode(
        {'username': username, }, settings.SECRET_KEY, algorithm='HS256')

    otp = random.randint(1000, 9999)
    pending_otp_validation = PendingOtpValidation(
        username, password, otp)

    if cache.set(jwt_token,
                 json.dumps(pending_otp_validation._asdict()), nx=True, ex=300):
        otp_sender = DianaHost()
        otp_sender.send(otp)
        return jwt_token
    raise UserNameNotUnique
