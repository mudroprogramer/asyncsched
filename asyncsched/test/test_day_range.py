
import datetime
from tracemalloc import start
from freezegun import freeze_time
import pytz

from asyncsched.src.time_interval_core import DayRange


@freeze_time("2022-08-14 7:00:01")
def test_get_next_run_time_day_interval():
  sched = DayRange(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 8, 14, 8, 0, 0)