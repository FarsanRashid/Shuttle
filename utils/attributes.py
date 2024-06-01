from collections import namedtuple


STATUS = "status"
SUCCESS = "success"
FAILURE = "failure"

Response = namedtuple('Response', ['status', 'code', 'message'])

CODE_NON_UNIQUE_USER = "non_unique_user"
CODE_INVALID_JSON = "invalid_json"
CODE_WRONG_METHOD = "incorrect_method"
CODE_SERVER_EXCEPTION = "server_exception"
CODE_SIGNUP_INITIATED = "signup_initiated"
CODE_INVALID_TOKEN = "invalid_token"
CODE_INVALID_OTP = "incorrect_otp"
CODE_SIGNUP_VERIFIED = "signup_verified"
CODE_LOGIN_SUCCESS = "login_success"
CODE_INVALID_CREDENTIALS = "invalid_credentials"
CODE_INVALID_PAYLOAD = "invalid_payload"
CODE_MISSING_PARAMATER = "missing_paramater"


MESSAGE_NON_UNIQUE_USER = "username already exists"
MESSAGE_INVALID_JSON = "invalid json payload"
MESSAGE_WRONG_METHOD = "incorrect request method"
MESSAGE_SERVER_EXCEPTION = "server exception occurred"
MESSAGE_SIGNUP_INITIATED = "signup initiated successfully"
MESSAGE_INVALID_TOKEN = "token is invalid/expired"
MESSAGE_INVALID_OTP = "otp is incorrect/expired"
MESSAGE_SIGNUP_VERIFIED = "signup verified successfully"
MESSAGE_LOGIN_SUCCESS = "login successful"
MESSAGE_INVALID_CREDENTIALS = "username/password is incorrect"
MESSAGE_INVALID_PAYLOAD = "payload validation failed"
MESSAGE_MISSING_PARAMATER = "required query parameter is missing"


error_username_exists = Response(FAILURE,
                                 CODE_NON_UNIQUE_USER, MESSAGE_NON_UNIQUE_USER)._asdict()
error_invalid_json = Response(FAILURE,
                              CODE_INVALID_JSON, MESSAGE_INVALID_JSON)._asdict()
error_invalid_request_method = Response(FAILURE,
                                        CODE_WRONG_METHOD, MESSAGE_WRONG_METHOD)._asdict()
error_server_exception = Response(
    FAILURE, CODE_SERVER_EXCEPTION, MESSAGE_SERVER_EXCEPTION)._asdict()

error_invalid_token = Response(
    FAILURE, CODE_INVALID_TOKEN, MESSAGE_INVALID_TOKEN)._asdict()

error_incorrect_otp = Response(
    FAILURE, CODE_INVALID_OTP, MESSAGE_INVALID_OTP)._asdict()

error_invalid_payload = Response(
    FAILURE, CODE_INVALID_PAYLOAD, MESSAGE_INVALID_PAYLOAD)._asdict()


success_signup_initiate = Response(
    SUCCESS, CODE_SIGNUP_INITIATED, MESSAGE_SIGNUP_INITIATED)._asdict()

success_signup_verification = Response(
    SUCCESS, CODE_SIGNUP_VERIFIED, MESSAGE_SIGNUP_VERIFIED)._asdict()

success_login = Response(
    SUCCESS, CODE_LOGIN_SUCCESS, MESSAGE_LOGIN_SUCCESS)._asdict()

error_invalid_credentials = Response(
    FAILURE, CODE_INVALID_CREDENTIALS, MESSAGE_INVALID_CREDENTIALS)._asdict()

error_missing_paramater = Response(
    FAILURE, CODE_MISSING_PARAMATER, MESSAGE_MISSING_PARAMATER)._asdict()


TOKEN = "token"
SESSION_ID = "session_id"
OTP = "OTP"
USERNAME = "username"
PASSWORD = "password"
COUNTRY_DIAL_CODE = "country_code"
CONTACT_NUMBER = "contact_number"
AUTHORIZATION = "Authorization"
BEARER = "Bearer"
