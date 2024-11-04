from time import sleep, time
from threading import Thread, Lock

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
    (
            {'cmd': 'cat', 'shell': True, 'stdin': 'test123'},
            {'rc': 0, 'stdout': 'test123', 'stderr': None},
    ),
])
def test_subps(kwargs: dict, s: dict):
    from .ps import process
    r = process(**kwargs)
    assert r['rc'] == s['rc']
    assert r['stdout'] == s['stdout']
    assert r['stderr'] == s['stderr'] or (
            isinstance(r['stderr'], str) and
            isinstance(s['stderr'], str) and
            r['stderr'].find(s['stderr']) != -1
    )


def test_wait_for_threads():
    from .ps import wait_for_threads

    def _dummy_workload(s: int):
        sleep(s)

    threads = [
        Thread(target=_dummy_workload, args=[2]),
        Thread(target=_dummy_workload, args=[3]),
    ]

    for t in threads:
        t.start()

    wait_for_threads(threads)

    for t in threads:
        assert not t.is_alive()


def test_wait_for_threads_timeout():
    from .ps import wait_for_threads

    def _dummy_workload(s: int):
        sleep(s)

    threads = [
        Thread(target=_dummy_workload, args=[2]),
        Thread(target=_dummy_workload, args=[3]),
    ]

    for t in threads:
        t.start()

    wait_for_threads(threads, timeout=1)

    for t in threads:
        assert t.is_alive()

    wait_for_threads(threads)

    for t in threads:
        assert not t.is_alive()


def test_process_list_in_threads():
    from .ps import process_list_in_threads
    lock = Lock()
    results = []

    def _dummy_workload(s: int):
        sleep(s)
        with lock:
            results.append(s)

    start_time = time()
    workload = [1, 1, 1, 1]
    process_list_in_threads(callback=_dummy_workload, to_process=workload, key='s', parallel=4)
    elapsed = time() - start_time

    assert 1 < elapsed < 1.2
    assert len(results) == 4
