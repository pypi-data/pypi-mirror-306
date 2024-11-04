from os import environ


def mode_debug() -> bool:
    return 'DEBUG' in environ and environ['DEBUG'] == '1'
