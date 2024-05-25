from service_layer.exceptions import InvalidPayload
from utils.attributes import error_missing_field, error_invalid_json


def validate_payload(payload):
    if not all(payload):
        raise InvalidPayload(error_missing_field)

    if not all(isinstance(value, str)
               for value in payload):
        raise InvalidPayload(error_invalid_json)


def validate_signup(token, otp, cache):
    validate_payload((token, otp))
