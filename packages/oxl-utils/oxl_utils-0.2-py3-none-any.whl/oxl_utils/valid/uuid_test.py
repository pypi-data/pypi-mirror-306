import pytest

# pylint: disable=C0415

@pytest.mark.parametrize('v, s', [
    ('c9b7582c-a36d-40a3-a8b3-a1d2a3dec704', True),
    ('c9b7582c-a36d-40a3-a8b3-a1d2a3dec70x', False),
    ('c9b7582c-a36d-40a-ba8b3-a1d2a3dec704', False),
    ('abc', False),
    ('test', False),
    (True, False),
    (1, False),
])
def test_uuid4(v: str, s: bool):
    from .uuid import valid_uuid4
    assert valid_uuid4(v) == s
