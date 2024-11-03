from partial_date import PartialDate


def to_partial_date(
    value: str | PartialDate,
) -> PartialDate:
    if value is None:
        return None
    if isinstance(value, PartialDate):
        return value
    if isinstance(value, str):
        if value in ["", "Unknown"]:
            return None
        return PartialDate(value)
    msg = f"Invalid PartialDate: {value}"
    raise ValueError(msg)
