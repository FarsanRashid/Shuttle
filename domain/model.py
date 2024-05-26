from collections import namedtuple
from utils.attributes import (
    USERNAME,
    CONTACT_NUMBER,
    COUNTRY_DIAL_CODE,
    OTP,
    PASSWORD,)

PendingOtpValidation = namedtuple(
    'PendingOtpValidation', [USERNAME, PASSWORD, OTP, COUNTRY_DIAL_CODE, CONTACT_NUMBER])
