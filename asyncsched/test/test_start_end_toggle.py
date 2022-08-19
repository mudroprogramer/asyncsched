
import datetime
from tracemalloc import start
from freezegun import freeze_time
import pytz

from asyncsched.src.time_interval_core import WEEK_DAYS, StartEndToggle


@freeze_time("2022-08-13 7:00:01")
def test_get_DayRange_before_start():
  day = 'mon'
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day=day, end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 8, 15, 8, 0, 0)
  assert dt.weekday() == WEEK_DAYS.index('mon')
  
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day=day, end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  seconds = sched.seconds_to_next_run()
  assert seconds == 176399

@freeze_time("2022-08-15 8:00:00")
def test_get_DayRange_on_start():
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 8, 19, 17, 0, 0)
  
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  seconds = sched.seconds_to_next_run()
  assert seconds == 378000

@freeze_time("2022-08-16 7:00:01")
def test_get_DayRange_between_start_end():
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 8, 19, 17, 0, 0)
  
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  seconds = sched.seconds_to_next_run()
  assert seconds == 295199

@freeze_time("2022-08-19 17:00:00")
def test_get_DayRange_on_end():
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 8, 22, 8, 0, 0)
  
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  seconds = sched.seconds_to_next_run()
  assert seconds == 226800

@freeze_time("2022-08-20 17:00:00")
def test_get_DayRange_after_end():
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 8, 22, 8, 0, 0)
  
  sched = StartEndToggle(start_time=datetime.time(8, 0), start_day='mon', end_time=datetime.time(17, 0), end_day='fri', timezone=pytz.utc)
  seconds = sched.seconds_to_next_run()
  assert seconds == 140400

