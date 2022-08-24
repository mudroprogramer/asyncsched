import datetime
from operator import index
from typing import List, Tuple

import pytz

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
            self.last_run_dt = self.dt_now()

        next_run = self.last_run_dt + self.interval_in_minutes + self.interval_in_seconds

        if next_run.time() < self.start_time:
            next_run = datetime.datetime.combine(next_run, self.start_time)

        if next_run.time() > self.end_time:
            next_run += datetime.timedelta(days=1)
            next_run = datetime.datetime.combine(next_run, self.start_time)

        while not self.is_day_legal(next_run):
            next_run += datetime.timedelta(days=1)
            next_run = datetime.datetime.combine(next_run, self.start_time)

        self.last_run_dt = next_run

        return next_run
    
    def seconds_to_next_run(self):
        return (self.get_next_run_datetime() - self.dt_now()).total_seconds()

    def dt_now(self):
        return datetime.datetime.now(tz=pytz.utc).astimezone(self.timezone).replace(tzinfo=None)

    def is_day_legal(self, dt):
        return WEEK_DAYS[dt.weekday()] in self.days_to_run

class DayInterval:
    def __init__(self, time_to_run: datetime.time, days_to_run: List[str] = WEEK_DAYS, timezone=None) -> None:
        self.time_to_run = time_to_run
        self.days_to_run = days_to_run
        self.last_run_dt = None
        self.timezone = timezone

    def get_next_run_datetime(self):
        if self.last_run_dt is None:
            next_run = datetime.datetime.combine(self.dt_now(), self.time_to_run)
            if next_run <= self.dt_now():
                next_run += datetime.timedelta(days=1)
        else:
            next_run = self.last_run_dt + datetime.timedelta(days=1)

        while not self.is_day_legal(next_run):
            next_run += datetime.timedelta(days=1)

        self.last_run_dt = next_run

        return next_run

    def seconds_to_next_run(self):
        return (self.get_next_run_datetime() - self.dt_now()).total_seconds()
    
    def dt_now(self):
        return datetime.datetime.now(tz=pytz.utc).astimezone(self.timezone).replace(tzinfo=None)

    def is_day_legal(self, dt):
        return WEEK_DAYS[dt.weekday()] in self.days_to_run

class Timer:
    def __init__(self, timezone=None):
        self.timezone = timezone
        self.last_run_dt = None

    def get_next_run_datetime(self):
        raise NotImplementedError

    def dt_now(self) -> datetime.datetime:
        return datetime.datetime.now(tz=pytz.utc).astimezone(self.timezone).replace(tzinfo=None)
    
    def seconds_to_next_run(self):
        return (self.get_next_run_datetime() - self.dt_now()).total_seconds()

class StartEndToggle(Timer):
    def __init__(self, start_time: datetime.time, start_day: str, end_time: datetime.time, end_day: str, timezone=None):
        super().__init__(timezone)
        self.start_time = start_time
        self.start_day = start_day
        self.end_time = end_time
        self.end_day = end_day

    def get_next_run_datetime(self):
        next_run = self.dt_now()

        next_start_dt = self.get_next_start_dt(next_run)

        next_end_dt = self.get_next_end_dt(next_run)

        if (next_start_dt <= next_end_dt):
            next_run = next_start_dt

        if (next_start_dt > next_end_dt):
            is_init = (self.last_run_dt is None)
            if (is_init):
                pass
            else:
                next_run = next_end_dt

        self.last_run_dt = next_run

        return next_run

    def get_next_start_dt(self, next_run_dt):

        next_start_dt = self.get_next_dt(next_run_dt, self.start_day, self.start_time)

        return next_start_dt

    def get_next_end_dt(self, next_run_dt):

        next_end_dt = self.get_next_dt(next_run_dt, self.end_day, self.end_time)

        return next_end_dt

    def get_next_dt(self, next_run_dt, day, time):
        days_to_end_day = (WEEK_DAYS.index(day) - next_run_dt.weekday()) % 7
        next_end_dt = datetime.datetime.combine(next_run_dt, time) + datetime.timedelta(days=days_to_end_day)
        if next_end_dt <= next_run_dt:
            next_end_dt += datetime.timedelta(days=7)
        return next_end_dt