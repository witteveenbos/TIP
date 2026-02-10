from datetime import datetime, timedelta
from typing import List

def hourly_datetime_labels() -> List[str]:
    """
    Return a list of 8760 hourly strings for a non-leap year, excluding the year
    and using a space as separator. Format: "MM-DD HH".
    - Always 8760 entries (assumes a 365-day year).
    - Uses only the standard library and naive datetimes.
    """
    # Use a representative non-leap year as the base (any non-leap year works)
    base_year = 2021
    start = datetime(base_year, 1, 1, 0, 0, 0)
    hours = 24 * 365  # 8760
    fmt = "%m-%d %H"
    return [(start + timedelta(hours=i)).strftime(fmt) for i in range(hours)]