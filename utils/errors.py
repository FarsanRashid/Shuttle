from collections import namedtuple

ERROR = 'error'

Error = namedtuple('Error', ['code', 'message'])

ERROR_MISSING_FIELD = Error("001", "Missing required fields")._asdict()
ERROR_USERNAME_EXISTS = Error("002", "Username already exists")._asdict()
ERROR_INVALID_JSON = Error("003", "Invalid JSON")._asdict()
ERROR_INVALID_REQUEST_METHOD = Error("004", "Invalid request method")._asdict()
