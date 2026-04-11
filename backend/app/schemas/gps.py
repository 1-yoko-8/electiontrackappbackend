@field_validator("timestamp")
def convert_to_ist_naive(cls, v):
    if v.tzinfo is None:
        raise ValueError("Timestamp must be timezone-aware")

    # Convert to IST first (safety)
    from zoneinfo import ZoneInfo
    v = v.astimezone(ZoneInfo("Asia/Kolkata"))

    # Remove timezone info → store as plain IST
    return v.replace(tzinfo=None)