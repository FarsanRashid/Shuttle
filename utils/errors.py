from collections import namedtuple


ERROR = namedtuple('Error', ['code', 'message'])

ERROR_MISSING_FIELD = ERROR("001", "Missing required fields")._asdict()
ERROR_USERNAME_EXISTS = ERROR("002", "Username already exists")._asdict()
ERROR_INVALID_JSON = ERROR("003", "Invalid JSON")._asdict()
ERROR_INVALID_REQUEST_METHOD = ERROR("004", "Invalid request method")._asdict()
