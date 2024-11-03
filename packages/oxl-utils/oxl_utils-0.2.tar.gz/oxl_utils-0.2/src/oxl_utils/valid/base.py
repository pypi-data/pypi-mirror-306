from re import match as regex_match


def _reg_match(reg, v: (str, None)) -> bool:
    if v is None:
        v = ''

    if isinstance(reg, str):
        return regex_match(reg, v) is not None

    return reg.match(v) is not None
