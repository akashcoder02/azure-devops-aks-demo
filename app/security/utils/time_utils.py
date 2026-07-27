from datetime import datetime
from zoneinfo import ZoneInfo


def get_scan_time():

    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%Y-%m-%d %H:%M:%S IST"
    )