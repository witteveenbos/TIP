from datetime import datetime, timedelta

def hourly_datetime_objects() -> list[datetime]:
    """
    Return a list of 8760 hourly datetime objects for a non-leap year.
    - Always 8760 entries (assumes a 365-day year).
    - Uses a representative non-leap year as the base (2021).
    When serialized via plotly's fig.to_dict(), these become ISO 8601 strings
    that the plotly React frontend understands natively.
    """
    base_year = 2021
    start = datetime(base_year, 1, 1, 0, 0, 0)
    hours = 24 * 365  # 8760
    return [start + timedelta(hours=i) for i in range(hours)]