import pytest

# pylint: disable=C0415


@pytest.mark.parametrize('v, r', [
    ('', True),
    (' ', True),
    ('                ', True),
    (None, True),
    ('test', False),
    (1, False),
    (True, False),
    ('None', False),
])
def test_null(v: any, r: bool):
    from .state import is_null
    assert is_null(v) == r


@pytest.mark.parametrize('v, r', [
    ('', False),
    (' ', False),
    ('                ', False),
    (None, False),
    ('test', True),
    (1, True),
    (True, True),
    ('None', True),
])
def test_set(v: any, r: bool):
    from .state import is_set
    assert is_set(v) == r
