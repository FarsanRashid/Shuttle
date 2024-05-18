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


SUCCESS_CODE = "000"
SUCCESS_SIGNUP = Response(
    SUCCESS, SUCCESS_CODE, "User created successfully")._asdict()
