from abc import ABC, abstractmethod
import logging
import os

import requests

from utils.attributes import BEARER, MESSAGE_SERVER_EXCEPTION
from utils.config import SIGNUP_OTP_TTL

logger = logging.getLogger(__name__)


class InvalidCountryDialCode(Exception):
    pass


class AbstractSMSSender(ABC):
    @abstractmethod
    def send(self, contact: str, otp: str):
        raise NotImplementedError


class DianaHost(AbstractSMSSender):
    def __init__(self):
        self.country_dial_code = "880"

    def send(self, contact: str, otp: str):
        api_url = "https://login.esms.com.bd/api/v3/sms/send"
        headers = {
            "Authorization": f"{BEARER} {os.getenv("DIANA_SMS_API_KEY")}",
            "Accept": "application/json",
        }
        _data = {
            "recipient": contact,
            "sender_id": os.getenv("DIANA_SMS_API_SENDER_ID"),
            "type": "plain",
            "message": f"Your shuttle verification code is {otp}. The code will expire in {SIGNUP_OTP_TTL // 60} minutes."
        }

        encoded_url = api_url + "?" + f"recipient={self.country_dial_code}" + \
            _data["recipient"] + "&sender_id=" + \
            _data["sender_id"] + "&type=" + _data["type"] \
            + "&message=" + _data["message"]

        response = requests.post(
            encoded_url, headers=headers, data=str(_data))
        if response.json().get("status") != "success":
            logger.exception(response.json())
            raise Exception(MESSAGE_SERVER_EXCEPTION)
        logger.info(response.json())


def get_sms_sender(country_dial_code: str) -> AbstractSMSSender:
    if country_dial_code == "880" or "+880":
        return DianaHost()
    raise InvalidCountryDialCode
