from datetime import datetime


def get_rfc3339_str(dt: datetime):
    return dt.replace(microsecond=0).astimezone().isoformat()
