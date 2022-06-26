from datetime import datetime


def datetime_check(string, pattern):
    try:
        datetime.strptime(string, pattern)
        return True
    except (Exception, ValueError):
        return False
