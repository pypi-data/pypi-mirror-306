from socket import socket, AF_INET, AF_INET6, SOCK_STREAM
from os import environ

from dns.resolver import Resolver, NoAnswer, NXDOMAIN, LifetimeTimeout, NoNameservers
from dns.exception import SyntaxError as DNSSyntaxError

from .valid.net import valid_ip

DEFAULT_NAMESERVERS = ['1.1.1.1', '8.8.8.8']
NS_ENV_KEY = 'NAMESERVERS'

dns_resolver = Resolver(configure=False)
dns_resolver.lifetime = 0.1
dns_resolver.timeout = 0.1

dns_resolver.nameservers = environ[NS_ENV_KEY].split(',') if NS_ENV_KEY in environ else DEFAULT_NAMESERVERS


def resolve_dns(v: str, t: str = 'A', timeout: float = dns_resolver.timeout) -> list[str]:
    try:
        if t != 'PTR':
            r = [r.to_text() for r in dns_resolver.resolve(v, t, lifetime=timeout)]

        else:
            r = [r.to_text() for r in dns_resolver.resolve_address(v, lifetime=timeout)]

        r.sort()
        return r

    except (IndexError, NoAnswer, NXDOMAIN, DNSSyntaxError, NoNameservers, LifetimeTimeout):
        return []


CHECK_RECORDS = ['A', 'AAAA']


def resolve_first_ip(v: str, check: list = None) -> (str, None):
    if check is None or not isinstance(check, list):
        check = CHECK_RECORDS

    for rtype in check:
        r = resolve_dns(v, t=rtype)
        if len(r) > 0:
            return r[0]

    return None


def is_port_open(target: str, port: (str, int), timeout: int = 1) -> bool:
    ip = target
    if not valid_ip(target):
        ip = resolve_first_ip(target)
        if ip is None:
            return False

    ip_proto = AF_INET if ip.find(':') == -1 else AF_INET6

    with socket(ip_proto, SOCK_STREAM) as s:
        s.settimeout(timeout)
        return s.connect_ex((ip, int(port))) == 0
