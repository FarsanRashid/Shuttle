from service_layer.exceptions import InvalidPayload
from utils.attributes import error_missing_field


def validate_payload(payload):
    if not all(payload):
        raise InvalidPayload(error_missing_field)


def validate_signup(token, otp, cache):
    validate_payload((token, otp))
