import pytest

# pylint: disable=C0415


@pytest.mark.parametrize('v, s', [
    ('test@oxl.at', True),
    ('test@abc.oxl.at', False),
])
def test_email_dns(v: str, s: bool):
    from .email import has_mailserver
    assert has_mailserver(v) == s


@pytest.mark.parametrize('v, s', [
    ({'email': 'test@oxl.at', 'dns': False}, True),
    ({'email': 'tes t@oxl.at', 'dns': False}, False),
    ({'email': 'test@abc.oxl.at', 'dns': False}, True),
    ({'email': 'test@abc.oxl.at', 'dns': True}, False),
    ({'email': 'test+abc@oxl.at', 'dns': False}, True),
    ({'email': 'test_abc@oxl.at', 'dns': False}, True),
    ({'email': 'test!@oxl.at', 'dns': False}, False),
    ({'email': 'test<@oxl.at', 'dns': False}, False),
])
def test_email(v: dict, s: bool):
    from .email import valid_email
    assert valid_email(**v) == s
