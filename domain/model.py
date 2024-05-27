from collections import namedtuple

from utils.attributes import CONTACT_NUMBER, COUNTRY_DIAL_CODE, OTP, PASSWORD, USERNAME

PendingOtpValidation = namedtuple(
    'PendingOtpValidation', [USERNAME, PASSWORD, OTP, COUNTRY_DIAL_CODE, CONTACT_NUMBER])
