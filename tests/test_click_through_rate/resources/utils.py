import datetime
import random

import ibis


def get_frequent_values(
    table: ibis.Table,
    min_percentage: float = 0.0,
    cols_exclude: list[str] | list = [],
):
    """Get a dictionary of frequent values for each column in the given table.

    Parameters
    ----------
    table : ibis.Table
        The table to get frequent values from.
    min_percentage : float, default=0.0
        The minimum percentage of occurrences for a value to be included.
    cols_exclude : list[str] | list, default=[]
        The columns to exclude from the result.

    Returns
    -------
    dict[str, list]
        A dictionary with column names as keys and a list of frequent values as values.

    """
    values_dict = {}

    for col in table.columns:
        if col in cols_exclude:
            continue

        df_out = (
            table.select(col)
            .value_counts()
            .mutate(percent=lambda t: (t[f"{col}_count"] / t[f"{col}_count"].sum()) * 100)
            .filter(lambda t: t.percent >= min_percentage)
            .order_by(ibis.desc("percent"))
            .select(col)
            .execute()
        )

        values_dict[col] = list(df_out.values.ravel())

    return values_dict


def generate_random_timestamps(
    timestamp: str | datetime.datetime | None = None,
    size: int = 1,
    n_days: int = 0,
    to_string: bool = False,
    format: str = "%Y-%m-%d %H:%M:%S",
):
    """Generate random timestamps between a given timestamp and a number of days before.

    Parameters
    ----------
    timestamp : str | datetime.datetime | None, default=None
        The timestamp to start from. If None, use the current datetime.
    size : int, default=1
        The number of timestamps to generate.
    n_days : int, default=0
        The number of days to go back from the given timestamp.
    to_string : bool, default=False
        Whether to return the timestamps as strings or datetime objects.
    format : str, default="%Y-%m-%d %H:%M:%S"
        The format to use when converting the timestamp to a string.

    Returns
    -------
    list[datetime.datetime | str]
        A list of generated timestamps.

    """
    if timestamp is None:
        timestamp = datetime.datetime.now()

    if isinstance(timestamp, str):
        start_date = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    else:
        start_date = timestamp
    end_date = start_date - datetime.timedelta(days=n_days)

    timestamps = []
    for _ in range(size):
        random_date = start_date - datetime.timedelta(days=random.randint(0, (start_date - end_date).days))
        random_time = datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        timestamp_generated = datetime.datetime.combine(random_date, random_time)
        if to_string:
            timestamp_generated = timestamp_generated.strftime(format)

        timestamps.append(timestamp_generated)

    return timestamps
