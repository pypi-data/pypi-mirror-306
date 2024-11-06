from datetime import datetime, timedelta, timezone

def now(format='%Y-%m-%d %H:%M:%S'):
    KST = timezone(timedelta(hours=9))
    dt = datetime.now(KST).strftime(format)


    return dt
