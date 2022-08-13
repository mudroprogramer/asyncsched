import datetime
import logging
from freezegun import freeze_time
import pytz

from asyncsched.src.time_interval_core import DayInterval, TimeInterval


@freeze_time("2012-01-14 23:00:01")
def test_scheduler_get_next_run_dt_seconds():
  sched = TimeInterval(interval_in_seconds=1)
  dt = sched.get_next_run_datetime()
  target = datetime.datetime(2012, 1, 14, 23, 00, 2, tzinfo=pytz.utc).astimezone().replace(tzinfo=None)
  assert dt == target
  
@freeze_time("2022-08-12 20:00:01")
def test_scheduler_get_next_run_dt_seconds_timezone():
  sched = TimeInterval(interval_in_seconds=1, timezone=pytz.timezone('America/New_York'))
  seconds = sched.seconds_to_next_run()
  assert seconds == 1

  sched = TimeInterval(interval_in_seconds=1, timezone=pytz.timezone('America/Los_Angeles'))
  dt = sched.get_next_run_datetime()
  target = datetime.datetime(2022, 8, 12, 20, 00, 2, tzinfo=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles')).replace(tzinfo=None)
  assert dt == target

@freeze_time("2012-01-14 23:00:01")
def test_scheduler_get_next_run_dt_minutes():
  sched = TimeInterval(interval_in_minutes=30)
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2012, 1, 14, 23, 30, 1, tzinfo=pytz.utc).astimezone().replace(tzinfo=None)

  sched = TimeInterval(interval_in_minutes=122)
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2012, 1, 15, 1, 2, 1, tzinfo=pytz.utc).astimezone().replace(tzinfo=None)


@freeze_time("2022-07-19 23:00:01")
def test_scheduler_get_next_run_dt_day_filter():
  sched = TimeInterval(interval_in_minutes=30, days_to_run=['tue', 'wed'])
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2022, 7, 19, 23, 30, 1, tzinfo=pytz.utc).astimezone().replace(tzinfo=None)

  sched = TimeInterval(interval_in_minutes=60, days_to_run=['tue', 'wed'])
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2022, 7, 20, 0, 0, 1, tzinfo=pytz.utc).astimezone().replace(tzinfo=None)

  sched = TimeInterval(interval_in_minutes=60, days_to_run=['tue'], timezone=pytz.utc)
  dt = sched.get_next_run_datetime()

  assert dt == datetime.datetime(2022, 7, 26, 0, 0, 0)


def test_is_day_legal():
  sched = TimeInterval(interval_in_minutes=30, days_to_run=['wed'])
  assert sched.is_day_legal(datetime.datetime(2022, 7, 20, 0, 0, 0))

  sched = TimeInterval(interval_in_minutes=30, days_to_run=['tue', 'thu'])
  assert sched.is_day_legal(datetime.datetime(2022, 7, 19, 0, 0, 0))
  assert not sched.is_day_legal(datetime.datetime(2022, 7, 20, 0, 0, 0))
  assert sched.is_day_legal(datetime.datetime(2022, 7, 21, 0, 0, 0))


@freeze_time("2022-07-19 10:00:00")
def test_get_next_run_time_cap():
  sched = TimeInterval(time_interval=('9:30', '15:00'), timezone=pytz.timezone('US/Eastern'))
  dt = sched.get_next_run_datetime()
  sched.seconds_to_next_run()
  assert dt == datetime.datetime(2022, 7, 19, 9, 30, 0)

  sched = TimeInterval(time_interval=('9:30', '15:00'), timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  sched.seconds_to_next_run()
  assert dt == datetime.datetime(2022, 7, 19, 10, 0, 0)
  
  sched = TimeInterval(time_interval=('11:00', '15:00'), timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  sched.seconds_to_next_run()
  assert dt == datetime.datetime(2022, 7, 19, 11, 0, 0)

  sched = TimeInterval(time_interval=('2:00', '9:00'), timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  sched.seconds_to_next_run()
  assert dt == datetime.datetime(2022, 7, 20, 2, 0, 0)

@freeze_time("2022-07-19 7:00:01")
def test_get_next_run_time_day_interval():
  sched = DayInterval(time_to_run=datetime.time(9, 30))
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 7, 19, 9, 30, 0)

@freeze_time("2022-07-19 9:30:01")
def test_get_next_run_time_day_interval_wrong_day():
  sched = DayInterval(time_to_run=datetime.time(9, 30), days_to_run=['fri'], timezone=pytz.utc)
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 7, 22, 9, 30, 0)

  # sched = DayInterval(time_to_run=datetime.time(9, 30), days_to_run=['fri'])
  seconds = sched.seconds_to_next_run()
  assert seconds == (datetime.datetime(2022, 7, 29, 9, 30, 0) - datetime.datetime(2022, 7, 19, 9, 30, 1)).total_seconds()

@freeze_time("2022-07-19 9:30:01")
def test_get_next_run_time_day_interval_wrong_day_timezone():
  sched = DayInterval(time_to_run=datetime.time(9, 30), days_to_run=['fri'], timezone=pytz.timezone('US/Eastern'))

  seconds = sched.seconds_to_next_run()
  assert seconds == 273599

@freeze_time("2022-08-13 6:13:00")
def test_get_next_run_time_cap_greater(caplog):
  caplog.set_level(logging.INFO)
  sched = TimeInterval(time_interval=['8:00', '17:00'], interval_in_seconds=30, days_to_run="mon,tue,wed,thu,fri", timezone=pytz.timezone('America/New_York'))
  dt = sched.get_next_run_datetime()
  assert dt == datetime.datetime(2022, 8, 15, 8, 0, 0)

  sched = TimeInterval(time_interval=['8:00', '17:00'], interval_in_seconds=30, days_to_run="mon,tue,wed,thu,fri", timezone=pytz.timezone('America/New_York'))
  seconds = sched.seconds_to_next_run()
  target = 193620.0
  assert seconds == target

  
