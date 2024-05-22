from collections import namedtuple


STATUS = "status"
SUCCESS = "success"
FAILURE = "failure"

Response = namedtuple('Response', ['status', 'code', 'message'])

ERROR_MISSING_FIELD = Response(FAILURE,
                               "001", "Missing required fields")._asdict()
ERROR_USERNAME_EXISTS = Response(FAILURE,
                                 "002", "Username already exists")._asdict()
ERROR_INVALID_JSON = Response(FAILURE,
                              "003", "Invalid JSON")._asdict()
ERROR_INVALID_REQUEST_METHOD = Response(FAILURE,
                                        "004", "Invalid request method")._asdict()

ERROR_SERVER_EXCEPTION = Response(
    FAILURE, "005", "Server Exception")._asdict()


SUCCESS_CODE = "000"
SUCCESS_SIGNUP_INITIATE = Response(
    SUCCESS, SUCCESS_CODE, "Signup initialization successful")._asdict()

TOKEN = "token"
