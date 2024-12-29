def set_wait_for_update_if(query, is_true: bool):
    return query.with_for_update() if is_true else query

def raise_exception_if_none(it, e):
    if e is not None and it is None:
        raise e

