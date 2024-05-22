from collections import namedtuple


STATUS = "status"
SUCCESS = "success"
FAILURE = "failure"

Response = namedtuple('Response', ['status', 'code', 'message'])

CODE_MISSING_FIELD = "missing_field"
CODE_NON_UNIQUE_USER = "non_unique_user"
CODE_INVALID_JSON = "invalid_json"
CODE_WRONG_METHOD = "incorrect_method"
CODE_SERVER_EXCEPTION = "server_exception"
CODE_SIGNUP_INITIATED = "signup_initiated"


MESSAGE_MISSING_FIELD = "missing required fields"
MESSAGE_NON_UNIQUE_USER = "username already exists"
MESSAGE_INVALID_JSON = "invalid json payload"
MESSAGE_WRONG_METHOD = "incorrect request method"
MESSAGE_SERVER_EXCEPTION = "server exception occurred"
MESSAGE_SIGNUP_INITIATED = "signup initiated successfully"


error_missing_field = Response(FAILURE,
                               CODE_MISSING_FIELD, MESSAGE_MISSING_FIELD)._asdict()
error_username_exists = Response(FAILURE,
                                 CODE_NON_UNIQUE_USER, MESSAGE_NON_UNIQUE_USER)._asdict()
error_invalid_json = Response(FAILURE,
                              CODE_INVALID_JSON, MESSAGE_INVALID_JSON)._asdict()
error_invalid_request_method = Response(FAILURE,
                                        CODE_WRONG_METHOD, MESSAGE_WRONG_METHOD)._asdict()
error_server_exception = Response(
    FAILURE, CODE_SERVER_EXCEPTION, MESSAGE_SERVER_EXCEPTION)._asdict()


success_signup_initiate = Response(
    SUCCESS, CODE_SIGNUP_INITIATED, MESSAGE_SIGNUP_INITIATED)._asdict()

TOKEN = "token"
OTP = "OTP"
USERNAME = "username"
PASSWORD = "password"
COUNTRY_CODE = "country_code"
CONTACT_NUMBER = "contact_number"
