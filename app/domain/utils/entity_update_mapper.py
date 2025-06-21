def _is_valid(value):
    if value is None:
        return False
    if isinstance(value, (str, list, dict)) and not value:
        return False
    return True


def extract_non_null_fields(entity: object, exclude: set[str] = None) -> dict:
    exclude = exclude or set()

    return {
        key: value
        for key, value in vars(entity).items()
        if key not in exclude and _is_valid(value)
    }
