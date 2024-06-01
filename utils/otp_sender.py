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
        self.__country_dial_code = "880"
        self.__api_url = "https://login.esms.com.bd/api/v3/sms/send"
        self.__headers = {
            "Authorization": f"{BEARER} {os.getenv("DIANA_SMS_API_KEY")}",
            "Accept": "application/json",
        }
        self.__sender_id = os.getenv("DIANA_SMS_API_SENDER_ID")
        self.__type = "plain"

    def send(self, contact: str, otp: str):
        try:
            _data = {
                "recipient": contact,
                "sender_id": self.__sender_id,
                "type": self.__type,
                "message": f"Your shuttle verification code is {otp}. The code will expire in {SIGNUP_OTP_TTL // 60} minutes."
            }

            encoded_url = self.__api_url + "?" + f"recipient={self.__country_dial_code}" + \
                _data["recipient"] + "&sender_id=" + \
                _data["sender_id"] + "&type=" + _data["type"] \
                + "&message=" + _data["message"]

            response = requests.post(
                encoded_url, headers=self.__headers, data=str(_data), timeout=5)

            if response.json().get("status") != "success":
                logger.exception(response.json())
                raise Exception(MESSAGE_SERVER_EXCEPTION)

            logger.info(response.json())

        except Exception as e:
            logger.exception(e)
            raise Exception(MESSAGE_SERVER_EXCEPTION)


def get_sms_sender(country_dial_code: str) -> AbstractSMSSender:
    if country_dial_code == "880" or "+880":
        return DianaHost()
    raise InvalidCountryDialCode
