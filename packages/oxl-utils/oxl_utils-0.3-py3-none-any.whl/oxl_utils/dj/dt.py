from os import environ
from datetime import datetime

from pytz import utc, timezone


# pylint: disable=W0707,R0801
def datetime_from_db(dt: (datetime, None), tz: (timezone, str) = None) -> (datetime, None):
    if not isinstance(dt, datetime):
        return None

    if tz in [None, '']:
        try:
            tz = environ['TIMEZONE']

        except KeyError:
            raise EnvironmentError('TIMEZONE not provided')

    if isinstance(tz, str):
        tz = timezone(tz)

    # datetime form db will always be UTC; convert it
    local_dt = dt.replace(tzinfo=utc).astimezone(tz)
    return tz.normalize(local_dt)
