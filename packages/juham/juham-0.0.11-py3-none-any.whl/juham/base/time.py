"""Time management for Juham framework."""

import datetime


def quantize(quanta: float, value: float):
    """Quantize the given value.

    Args:
        quanta (float): resolution for quantization
        value (float): value to be quantized

    Returns:
        (float): quantized value

    Example:
    ::

        hour_of_a_day = quantize(3600, epoch_seconds)
    """
    return (value // quanta) * quanta


def epoc2utc(epoch):
    """Converts the given epoch time to UTC time string. All time
    coordinates are represented in UTC time. This allows the time
    coordinate to be mapped to any local time representation without
    ambiguity.

    Args:
        epoch (float) : timestamp in UTC time
        rc (str): time string describing date, time and time zone e.g 2024-07-08T12:10:22Z

    Returns:
        UTC time
    """
    utc_time = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc)
    utc_timestr = utc_time.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    return utc_timestr


def timestampstr(ts: float):
    """Converts the given timestamp to human readable string of format 'Y-m-d
    H:M:S'.

    Args:
        ts (timestamp):  time stamp to be converted

    Returns:
        rc (string):  human readable date-time string
    """
    return str(datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"))


def timestamp():
    """Returns the current date-time in UTC.

    Returns:
        rc (datetime):  datetime in UTC.
    """
    return datetime.datetime.now(datetime.timezone.utc).timestamp()


def timestamp_hour(ts: float):
    """Returns the hour in 24h format in UTC.

    Args:
        ts (float): timestamp
    Returns:
        rc (int):  current hour in UTC 0 ...23
    """
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.hour


def is_time_between(begin_time, end_time, check_time=None):
    """Check if the given time is within the given time line. All
    timestamps must be in UTC time.

    Args:
        begin_time (timestamp):  beginning of the timeline
        end_time (timestamp):  end of the timeline
        check_time (timestamp):  time to be checked

    Returns:
        rc (bool):  True if within the timeline
    """

    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def elapsed_seconds_in_hour(ts_utc: float) -> float:
    """Given timestamp in UTC, Compute elapsed seconds within an hour

    Args:
        ts  (float) : seconds since UTC epoch
    Returns:
        float: _description_
    """

    ts = datetime.datetime.fromtimestamp(ts_utc)
    # Define start time (for example 9:15:30)
    start_time = ts.replace(minute=15, second=30, microsecond=0)

    # Compute the difference between the times
    elapsed_time = ts - start_time

    # Convert the difference to seconds
    return elapsed_time.total_seconds()


def elapsed_seconds_in_day(ts_utc: float) -> float:
    """Fetch the elapsed seconds since the be given time stamp 'ts_utc'.

    Returns:
        float: elapsed second today
    """
    # Convert the float timestamp into a datetime object
    timestamp_datetime = datetime.datetime.fromtimestamp(ts_utc)
    # Get the start of today (midnight)
    midnight = datetime.datetime.combine(timestamp_datetime.date(), datetime.time())
    # Calculate the elapsed seconds since midnight
    elapsed_seconds = (timestamp_datetime - midnight).total_seconds()
    return elapsed_seconds
