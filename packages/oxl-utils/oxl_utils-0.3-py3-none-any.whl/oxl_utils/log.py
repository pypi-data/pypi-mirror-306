from os import getpid, environ
from sys import stderr, stdout
from inspect import stack as inspect_stack
from inspect import getfile as inspect_getfile

from .dt import datetime_w_tz
from .debug import mode_debug

LOG_FORMAT = 'default' if 'LOG_FORMAT' not in environ else environ['LOG_FORMAT']
LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S %z'
PID = getpid()

LEVEL_NAME_MAPPING = {
    1: 'FATAL',
    2: 'ERROR',
    3: 'WARN',
    4: 'INFO',
    5: 'INFO',
    6: 'DEBUG',
    7: 'DEBUG',
}


def _log_formatted(level: int, msg: str, mid: str = '') -> str:
    if LOG_FORMAT == 'gunicorn':
        return f"[{datetime_w_tz().strftime(LOG_TIME_FORMAT)}] [{PID}] [{LEVEL_NAME_MAPPING[level]}] {mid}{msg}"

    return f"{datetime_w_tz().strftime(LOG_TIME_FORMAT)} {LEVEL_NAME_MAPPING[level]} {mid}{msg}"


def log(msg: str, level: int = 3):
    debug = mode_debug()
    prefix_caller = ''

    if level > 5 and not debug:
        return

    if debug:
        caller = inspect_getfile(inspect_stack()[1][0]).rsplit('/', 1)[1].rsplit('.', 1)[0]
        prefix_caller = f'[{caller}] '

    stdout.write(_log_formatted(msg=msg, level=level, mid=prefix_caller))


def log_warn(msg: str, _stderr: bool = False):
    msg = f'\x1b[1;33m{_log_formatted(msg=msg, level=3)}\x1b[0m\n'

    if _stderr:
        stderr.write(msg)

    else:
        stdout.write(msg)


def log_error(msg: str):
    stderr.write(f'\033[01;{_log_formatted(msg=msg, level=2)}\x1b[0m\n')
