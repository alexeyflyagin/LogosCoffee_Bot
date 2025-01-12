def set_with_for_update_if(query, is_true: bool):
    return query.with_for_update() if is_true else query
