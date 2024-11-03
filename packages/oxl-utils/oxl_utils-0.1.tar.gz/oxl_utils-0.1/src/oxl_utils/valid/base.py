def _reg_match(reg, v: (str, None)) -> bool:
    if v is None:
        v = ''

    return reg.match(v) is not None
