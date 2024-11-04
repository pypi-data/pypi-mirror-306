import re as regex

from .base import _reg_match

# source: https://validators.readthedocs.io/en/latest/_modules/validators/domain.html#domain
MATCH_DOMAIN = regex.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)


def valid_domain(value: str) -> bool:
    return _reg_match(reg=MATCH_DOMAIN, v=value)
