def is_null(data) -> bool:
    if data is None:
        return True

    return str(data).strip() == ''


def is_set(data: str) -> bool:
    return not is_null(data)
