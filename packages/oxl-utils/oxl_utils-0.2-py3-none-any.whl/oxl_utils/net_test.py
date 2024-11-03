import pytest

# pylint: disable=C0415


@pytest.mark.parametrize('v, s', [
    (
            {'v': 'oxl.at', 't': 'A'},
            {'exist': True, 'len': 1},
    ),
    (
            {'v': 'oxl.at', 't': 'AAAA'},
            {'exist': True, 'len': 1},
    ),
    (
            {'v': 'xyz.oxl.at', 't': 'MX'},
            {'exist': False, 'len': 0},
    ),
    (
            {'v': 'xyz.oxl.at', 't': 'MX'},
            {'exist': False, 'len': 0},
    ),
    (
            {'v': '1.1.1.1', 't': 'PTR'},
            {'exist': True, 'len': 1, 'v': ['one.one.one.one.']},
    ),
    (
            {'v': 'one.one.one.one', 't': 'A'},
            {'exist': True, 'len': 2, 'v': ['1.0.0.1', '1.1.1.1']},
    ),
])
def test_dns(v: dict, s: dict):
    from .net import resolve_dns
    r = resolve_dns(**v, timeout=2.0)
    assert (len(r) > 0) == s['exist']
    assert len(r) == s['len']
    if 'v' in s:
        assert r == s['v']


@pytest.mark.parametrize('v, s', [
    ({'v': 'one.one.one.one'}, '1.0.0.1'),
    ({'v': 'test.abc.sldjflsdkl.sdlfj'}, None),
    ({'v': 'one.one.one.one', 'check': ['AAAA', 'A']}, '2606:4700:4700::1001'),
])
def test_dns_first_ip(v: dict, s: str):
    from .net import resolve_first_ip
    assert resolve_first_ip(**v) == s


@pytest.mark.parametrize('v, s', [
    (
            {'target': '1.1.1.1', 'port': 53},
            True,
    ),
    (
            {'target': '1.1.1.1', 'port': 54},
            False,
    ),
    (
            {'target': 'one.one.one.one', 'port': 53},
            True,
    ),
])
def test_port(v: dict, s: bool):
    from .net import is_port_open
    assert is_port_open(**v) == s
