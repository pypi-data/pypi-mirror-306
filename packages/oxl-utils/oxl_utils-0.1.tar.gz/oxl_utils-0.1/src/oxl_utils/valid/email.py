import re as regex

from ..net import resolve_dns
from .base import _reg_match
from .dns import valid_domain

EMAIL_REGEX_USER = regex.compile(r"^[a-zA-Z0-9_+~\-\.]*$")


def has_mailserver(email: str, dns: bool = True) -> bool:
    if not isinstance(email, str):
        return False

    if not dns:
        return True

    domain = email.split('@', 1)[1]
    return len(resolve_dns(domain, t='MX')) > 0


def valid_email(email: str, dns: bool = False) -> bool:
    if not email or not isinstance(email, str) or '@' not in email:
        return False

    user_part, domain_part = email.rsplit('@', 1)

    if not _reg_match(reg=EMAIL_REGEX_USER, v=user_part):
        return False

    if not valid_domain(domain_part):
        return False

    return has_mailserver(email=email, dns=dns)
