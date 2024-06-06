from service_layer.exceptions import SearchQueryTooShortError


def sanitize(input):
    sanitized_value = input.strip().lower()
    if len(sanitized_value) < 3:
        raise SearchQueryTooShortError
    return sanitized_value
