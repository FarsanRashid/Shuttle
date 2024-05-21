from collections import namedtuple
import json
import random

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

    jwt_token = jwt.encode(
        {'username': username, }, settings.SECRET_KEY, algorithm='HS256')

    user = cache.get(jwt_token)

    if user is not None or Passenger.objects.filter(username=username).exists():
        raise UserNameNotUnique

    pending_otp_validation = PendingOtpValidation(
        username, password, random.randint(1000, 9999))

    cache.set(jwt_token,
              json.dumps(pending_otp_validation._asdict()), ex=300)
