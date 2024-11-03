import pytest

# pylint: disable=C0415


@pytest.mark.parametrize('kwargs, s', [
    (
            {'cmd': 'echo abc'},
            {'rc': 0, 'stdout': 'abc', 'stderr': None},
    ),
    (
            {'cmd': ['echo', 'abc']},
            {'rc': 0, 'stdout': 'abc', 'stderr': None},
    ),
    (
            {'cmd': ['echo', 'abc'], 'shell': True},
            {'rc': 0, 'stdout': 'abc', 'stderr': None},
    ),
    (
            {'cmd': 'echo abc', 'shell': True},
            {'rc': 0, 'stdout': 'abc', 'stderr': None},
    ),
    (
            {'cmd': 'sleep 1'},
            {'rc': 0, 'stdout': None, 'stderr': None},
    ),
    (
            {'cmd': 'sleep 1', 'timeout_sec': 0},
            {'rc': 1, 'stdout': None, 'stderr': 'timed out'},
    ),
    (
            {'cmd': 'sleep 1', 'timeout_sec': 0, 'shell': True},
            {'rc': 1, 'stdout': None, 'stderr': 'timed out'},
    ),
    (
            {'cmd': 'sleep 1', 'timeout_sec': 0, 'shell': True, 'timeout_shell': False},
            {'rc': 1, 'stdout': None, 'stderr': 'timed out'},
    ),
    (
            {'cmd': 'mkdir /tmp/abc/def/ghi'},
            {'rc': 1, 'stdout': None, 'stderr': 'No such file or directory'},
    ),
    (
            {'cmd': 'echo', 'empty_none': False},
            {'rc': 0, 'stdout': '', 'stderr': ''},
    ),
])
def test_subps(kwargs: dict, s: dict):
    from .subps import process
    r = process(**kwargs)
    assert r['rc'] == s['rc']
    assert r['stdout'] == s['stdout']
    assert r['stderr'] == s['stderr'] or (
            isinstance(r['stderr'], str) and
            isinstance(s['stderr'], str) and
            r['stderr'].find(s['stderr']) != -1
    )
