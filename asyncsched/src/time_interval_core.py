
from dataclasses import dataclass
import datetime
from typing import List, Tuple
import zoneinfo

from pytz import timezone

WEEK_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


class TimeInterval:

    def __init__(self, time_interval: Tuple[str] = ('min', 'max'), interval_in_seconds: int = 0, interval_in_minutes: int = 0, days_to_run: List[str] = WEEK_DAYS, timezone=None) -> None:
        self.interval_in_seconds = datetime.timedelta(seconds=interval_in_seconds)
        self.interval_in_minutes = datetime.timedelta(minutes=interval_in_minutes)
        self.days_to_run = days_to_run
        self.last_run_dt = None
        self.timezone = timezone

        T = time_interval[0]
        self.start_time = datetime.time.min if T == 'min' else datetime.time(*[int(x) for x in T.split(':')])
        T = time_interval[1]
        self.end_time = datetime.time.max if T == 'max' else datetime.time(*[int(x) for x in T.split(':')])

    def get_next_run_datetime(self):
        if self.last_run_dt is None:
            self.last_run_dt = datetime.datetime.now(tz=self.timezone)

        next_run = self.last_run_dt + self.interval_in_minutes + self.interval_in_seconds

        while not self.is_day_legal(next_run):
            next_run = next_run + datetime.timedelta(days=1)
            next_run = datetime.datetime.combine(next_run, datetime.time(0, 0))

        capped_time = self.cap_to_time_interval(next_run.time())
        next_run = datetime.datetime.combine(next_run, capped_time)

        self.last_run_dt = next_run

        return next_run
    
    def seconds_to_next_run(self):
        return (self.get_next_run_datetime() - datetime.datetime.now(tz=self.timezone).replace(tzinfo=None)).total_seconds()

    def is_day_legal(self, dt):
        return WEEK_DAYS[dt.weekday()] in self.days_to_run

    def cap_to_time_interval(self, time: datetime.time):
        if time < self.start_time:
            return self.start_time

        if time > self.end_time:
            return self.end_time

        return time

class DayInterval:
    def __init__(self, time_to_run: datetime.time, days_to_run: List[str] = WEEK_DAYS, timezone=None) -> None:
        self.time_to_run = time_to_run
        self.days_to_run = days_to_run
        self.last_run_dt = None
        self.timezone = timezone

    def get_next_run_datetime(self):
        if self.last_run_dt is None:
            next_run = datetime.datetime.combine(datetime.datetime.now(tz=self.timezone), self.time_to_run)
            if next_run <= datetime.datetime.now(tz=self.timezone).replace(tzinfo=None):
                next_run += datetime.timedelta(days=1)
        else:
            next_run = self.last_run_dt + datetime.timedelta(days=1)

        while not self.is_day_legal(next_run):
            next_run += datetime.timedelta(days=1)

        self.last_run_dt = next_run

        return next_run

    def seconds_to_next_run(self):
        return (self.get_next_run_datetime() - datetime.datetime.now(tz=self.timezone).replace(tzinfo=None)).total_seconds()
    
    def is_day_legal(self, dt):
        return WEEK_DAYS[dt.weekday()] in self.days_to_run

