import subprocess
from time import sleep, time
from pathlib import Path
from os import environ, getcwd
from functools import cache
from threading import Thread

from .log import log

# pylint: disable=R0914,R0912
def process(
        cmd: (str, list), timeout_sec: int = None, shell: bool = False, timeout_shell: bool = True,
        cwd: Path = None, env: dict = None, env_inherit: bool = False, env_remove: list = None,
        empty_none: bool = True, stdin: str = None,
) -> dict:
    if cwd is None:
        cwd = getcwd()

    cmd_str = cmd
    if isinstance(cmd, list):
        cmd_str = ' '.join(cmd)

    if shell:
        cmd = cmd_str
        if timeout_shell and timeout_sec is not None:
            cmd = f'timeout {timeout_sec} {cmd}'

    elif not isinstance(cmd, list):
        cmd = cmd.split(' ')

    log(msg=f"Executing command: '{cmd_str}'", level=6)

    if env is None:
        env = {}

    if env_inherit:
        if env_remove is None:
            env_remove = []

        # merge provided env with current env
        env = {**environ.copy(), **env}
        for k in env_remove:
            if k in env:
                env.pop(k)

    try:
        with subprocess.Popen(
            cmd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            cwd=cwd,
            env=env,
        ) as p:
            if stdin is not None:
                b_stdout, b_stderr = p.communicate(timeout=timeout_sec, input=stdin.encode('utf-8'))

            else:
                b_stdout, b_stderr = p.communicate(timeout=timeout_sec)

            stdout, stderr, rc = b_stdout.decode('utf-8').strip(), b_stderr.decode('utf-8').strip(), p.returncode

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, subprocess.CalledProcessError,
            OSError, IOError) as error:
        stdout, stderr, rc = '', str(error), 1


    if empty_none:
        if stdout.strip() == '':
            stdout = None

        if stderr.strip() == '':
            stderr = None

    return {
        'stdout': stdout,
        'stderr': stderr,
        'rc': rc,
    }


@cache
def process_with_cache(
        cmd: (str, list), timeout_sec: int = None, shell: bool = False, timeout_shell: bool = True,
        cwd: Path = None, env: dict = None, env_inherit: bool = False, env_remove: list = None,
        empty_none: bool = True, stdin: str = None,
) -> dict:
    # read-only commands which results can be cached
    return process(
        cmd=cmd, timeout_sec=timeout_sec, shell=shell, timeout_shell=timeout_shell, cwd=cwd,
        env=env, env_inherit=env_inherit, env_remove=env_remove, empty_none=empty_none, stdin=stdin,
    )


def wait_for_threads(threads: list[Thread], timeout: int = 600):
    break_time = time() + timeout
    threads_done = False

    while not threads_done and time() < break_time:
        threads_done = all(not t.is_alive() for t in threads)
        sleep(0.05)
