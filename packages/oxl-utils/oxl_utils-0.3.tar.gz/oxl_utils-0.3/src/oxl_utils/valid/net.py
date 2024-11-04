from ipaddress import ip_address, IPv4Address, IPv6Address, AddressValueError, \
    IPv4Network, IPv6Network, NetmaskValueError


def valid_ip(ip: str) -> bool:
    if not isinstance(ip, str):
        return False

    try:
        ip_address(ip)
        return True

    except (AddressValueError, ValueError):
        return False


def valid_ip4(ip: str) -> bool:
    if not isinstance(ip, str):
        return False

    try:
        IPv4Address(ip)
        return True

    except AddressValueError:
        return False


def valid_ip6(ip: str) -> bool:
    if not isinstance(ip, str):
        return False

    try:
        IPv6Address(ip)
        return True

    except AddressValueError:
        return False


def valid_net4(ip: str, strict: bool = False) -> bool:
    if not isinstance(ip, str):
        return False

    try:
        IPv4Network(ip, strict=strict)
        return True

    except (AddressValueError, NetmaskValueError):
        return False


def valid_net6(ip: str, strict: bool = False) -> bool:
    if not isinstance(ip, str):
        return False

    try:
        IPv6Network(ip, strict=strict)
        return True

    except (AddressValueError, NetmaskValueError):
        return False


def valid_public_ip(ip: str) -> bool:
    ip = str(ip)
    try:
        ip = IPv4Address(ip)
        return ip.is_global and \
            not ip.is_loopback and \
            not ip.is_reserved and \
            not ip.is_multicast and \
            not ip.is_link_local

    except AddressValueError:
        try:
            ip = IPv6Address(ip)
            return ip.is_global and \
                not ip.is_loopback and \
                not ip.is_reserved and \
                not ip.is_multicast and \
                not ip.is_link_local

        except AddressValueError:
            return False


def valid_asn(asn: str) -> bool:
    asn = str(asn)
    return asn.isdigit() and 0 <= int(asn) <= 4_294_967_294


def get_ipv(ip: str) -> int:
    if valid_ip4(ip):
        return 4

    return 6


def valid_port(p: (str, int)) -> bool:
    if isinstance(p, str):
        if not p.isnumeric():
            return False

        p = int(p)

    return 0 < p < 65536
