from datetime import datetime, timedelta


def days_before(x, ref_date=datetime.now()):
    return ref_date - timedelta(days=x)


# Alias for days_before
def days_ago(x):
    return days_before(x)


def days_after(x, ref_date=datetime.now()):
    return ref_date + timedelta(days=x)


# Alias for days_after
def days_since(x, ref_date=datetime.now()):
    return days_after(x, ref_date)


def tomorrow():
    return datetime.now() + timedelta(days=1)


def yesterday():
    return datetime.now() - timedelta(days=1)


def hours_before(x, ref_date=datetime.now()):
    return ref_date - timedelta(hours=x)


# Alias for hours_before
def hours_ago(x):
    return hours_before(x)


def hours_after(x, ref_date=datetime.now()):
    return ref_date + timedelta(hours=x)


# Alias for hours_after
def hours_since(x, ref_date=datetime.now()):
    return hours_after(x, ref_date)


def minutes_before(x, ref_date=datetime.now()):
    return ref_date - timedelta(minutes=x)


# Alias for minutes_before
def minutes_ago(x):
    return minutes_before(x)


def minutes_after(x, ref_date=datetime.now()):
    return ref_date + timedelta(minutes=x)


# Alias for minutes_after
def minutes_since(x, ref_date=datetime.now()):
    return minutes_after(x, ref_date)


def seconds_before(x, ref_date=datetime.now()):
    return ref_date - timedelta(minutes=x)


# Alias for seconds_before
def seconds_ago(x):
    return seconds_before(x)


def seconds_after(x, ref_date=datetime.now()):
    return ref_date + timedelta(minutes=x)


# Alias for seconds_after
def seconds_since(x, ref_date=datetime.now()):
    return seconds_after(x, ref_date)


def weeks_before(x, ref_date=datetime.now()):
    return ref_date - timedelta(weeks=x)


# Alias for seconds_before
def weeks_ago(x):
    return weeks_before(x)


def weeks_after(x, ref_date=datetime.now()):
    return ref_date + timedelta(weeks=x)


# Alias for seconds_after
def weeks_since(x, ref_date=datetime.now()):
    return weeks_after(x, ref_date)


# Internal method to support the month_* functions
def month_add(x, ref_date=datetime.now()):
    years_to_add = int((ref_date.month + x) / 12)
    months_to_add = (ref_date.month + x) % 12
    return datetime(ref_date.year + years_to_add, ref_date.month + months_to_add, ref_date.day, ref_date.hour, ref_date.minute, ref_date.second, ref_date.microsecond)


def months_before(x, ref_date=datetime.now()):
    return month_add(-1*x, ref_date)


# Alias for months_before
def months_ago(x):
    return months_before(x)


def months_after(x, ref_date=datetime.now()):
    return month_add(x, ref_date)


# Alias for months_after
def months_since(x, ref_date=datetime.now()):
    return months_after(x, ref_date)


def years_before(x, ref_date=datetime.now()):
    return datetime(ref_date.year - x, ref_date.month, ref_date.day, ref_date.hour, ref_date.minute, ref_date.second, ref_date.microsecond)


# Alias for years_before
def years_ago(x):
    return years_before(x)


def years_after(x, ref_date=datetime.now()):
    return datetime(ref_date.year + x, ref_date.month, ref_date.day, ref_date.hour, ref_date.minute, ref_date.second, ref_date.microsecond)


# Alias for years_after
def years_since(x, ref_date=datetime.now()):
    return years_after(x, ref_date)


