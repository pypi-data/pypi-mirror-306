from .base import _reg_match

UUID4_REGEX = r'^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$'


def valid_uuid4(data: str) -> bool:
    data = str(data)
    return _reg_match(reg=UUID4_REGEX, v=data)
