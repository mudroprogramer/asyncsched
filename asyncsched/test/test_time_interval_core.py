import datetime
from freezegun import freeze_time

from asyncsched.src.time_interval_core import TimeInterval

@freeze_time("2012-01-14 23:00:01")
def test_scheduler_get_next_run_dt_seconds():
  sched = TimeInterval(interval_in_seconds=1)
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2012, 1, 14, 23, 00, 2)


@freeze_time("2012-01-14 23:00:01")
def test_scheduler_get_next_run_dt_minutes():
  sched = TimeInterval(interval_in_minutes=30)
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2012, 1, 14, 23, 30, 1)

  sched = TimeInterval(interval_in_minutes=122)
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2012, 1, 15, 1, 2, 1)

@freeze_time("2022-07-19 23:00:01")
def test_scheduler_get_next_run_dt_day_filter():
  sched = TimeInterval(interval_in_minutes=30, days_to_run=['tue', 'wed'])
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2022, 7, 19, 23, 30, 1)

  sched = TimeInterval(interval_in_minutes=60, days_to_run=['tue', 'wed'])
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2022, 7, 20, 0, 0, 1)

  sched = TimeInterval(interval_in_minutes=60, days_to_run=['tue'])
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2022, 7, 26, 0, 0, 0)
  
def test_is_day_legal():
  sched = TimeInterval(interval_in_minutes=30, days_to_run=['wed'])
  assert sched.is_day_legal(datetime.datetime(2022, 7, 20, 0, 0, 0))

  sched = TimeInterval(interval_in_minutes=30, days_to_run=['tue', 'thu'])
  assert sched.is_day_legal(datetime.datetime(2022, 7, 19, 0, 0, 0))
  assert not sched.is_day_legal(datetime.datetime(2022, 7, 20, 0, 0, 0))
  assert sched.is_day_legal(datetime.datetime(2022, 7, 21, 0, 0, 0))

def test_cap_to_time_interval():
  sched = TimeInterval()
  time = sched.cap_to_time_interval(datetime.time(10, 0))
  
  assert time == datetime.time(10,0)
  
  sched = TimeInterval(time_interval=('9:30', '15:00'))
  time = sched.cap_to_time_interval(datetime.time(10, 0))
  assert time == datetime.time(10,0)
  
  time = sched.cap_to_time_interval(datetime.time(7, 0))
  assert time == datetime.time(9,30)
  
  time = sched.cap_to_time_interval(datetime.time(18, 0))
  assert time == datetime.time(15,00)