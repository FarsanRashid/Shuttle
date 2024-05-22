from collections import namedtuple
import json
import random

from django.conf import settings
import jwt
import redis

from accounts.models import Passenger


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

    pending_otp_validation = PendingOtpValidation(
        username, password, random.randint(1000, 9999))

    if cache.set(jwt_token,
                 json.dumps(pending_otp_validation._asdict()), nx=True, ex=300):
        return jwt_token
    raise UserNameNotUnique
