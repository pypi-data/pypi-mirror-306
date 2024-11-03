import pytest

# pylint: disable=C0415


@pytest.mark.parametrize('v, s', [
    ('1.1.1.1', True),
    ('192.168.0.1', True),
    ('::1', True),
    ('2adb::1', True),
    ('2adb:.:1', False),
    ('1.1.1:1', False),
    ('test', False),
    ('1', False),
    ('!', False),
    (True, False),
])
def test_ip(v: str, s: bool):
    from .net import valid_ip
    assert valid_ip(v) == s


@pytest.mark.parametrize('v, s', [
    ('1.1.1.1', True),
    ('192.168.0.1', True),
    ('::1', False),
    ('2adb::1', False),
    ('2adb:.:1', False),
    ('1.1.1:1', False),
    ('test', False),
    ('1', False),
    ('!', False),
    (True, False),
])
def test_ip4(v: str, s: bool):
    from .net import valid_ip4
    assert valid_ip4(v) == s


@pytest.mark.parametrize('v, s', [
    ('1.1.1.1', False),
    ('192.168.0.1', False),
    ('::1', True),
    ('2adb::1', True),
    ('2adb:.:1', False),
    ('1.1.1:1', False),
    ('test', False),
    ('1', False),
    ('!', False),
    (True, False),
])
def test_ip6(v: str, s: bool):
    from .net import valid_ip6
    assert valid_ip6(v) == s


@pytest.mark.parametrize('v, s', [
    ('1.1.1.1/32', True),
    ('192.168.10.0/24', True),
    ('1.1.1.1', True),
    ('192.168.0.1', True),
    ('::1', False),
    ('::1/128', False),
    ('2adb::1', False),
    ('2adb:.:1', False),
    ('1.1.1:1', False),
    ('test', False),
    ('1', False),
    ('!', False),
    (True, False),
])
def test_net4(v: str, s: bool):
    from .net import valid_net4
    assert valid_net4(v) == s


@pytest.mark.parametrize('v, s', [
    ('1.1.1.1/32', False),
    ('192.168.10.0/24', False),
    ('1.1.1.1', False),
    ('192.168.0.1', False),
    ('::1', True),
    ('::1/128', True),
    ('2adb::1', True),
    ('2adb::1/64', True),
    ('2adb:.:1', False),
    ('1.1.1:1', False),
    ('test', False),
    ('1', False),
    ('!', False),
    (True, False),
])
def test_net6(v: str, s: bool):
    from .net import valid_net6
    assert valid_net6(v) == s


@pytest.mark.parametrize('v, s', [
    ('1.1.1.1', True),
    ('192.168.0.1', False),
    ('::1', False),
    ('2adb::1', True),
    ('2adb:.:1', False),
    ('1.1.1:1', False),
    ('test', False),
    ('1', False),
    ('!', False),
    (True, False),
])
def test_public_ip(v: str, s: bool):
    from .net import valid_public_ip
    assert valid_public_ip(v) == s


@pytest.mark.parametrize('v, s', [
    (1337, True),
    ('a', False),
    (True, False),
    (3829229, True),
    (-1, False),
])
def test_asn(v: str, s: bool):
    from .net import valid_asn
    assert valid_asn(v) == s
