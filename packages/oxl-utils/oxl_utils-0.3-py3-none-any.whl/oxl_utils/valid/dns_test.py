import pytest

# pylint: disable=C0415

@pytest.mark.parametrize('v, s', [
    ('oxl.at', True),
    ('abc.oxl.at', True),
    ('!abc.oxl.at', False),
    ('abc.<oxl.at', False),
    ('abc. oxl.at', False),
    ('test@oxl.at', False),
    ('_dmarc.oxl.at', True),
    ('abc._dmarc.oxl.at', True),
])
def test_domain(v: str, s: bool):
    from .dns import valid_domain
    assert valid_domain(v) == s
