
import datetime
from typing import List, Tuple

WEEK_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


class TimeInterval:

    def __init__(self, time_interval: Tuple[str] = ('min', 'max'), interval_in_seconds: int = 0, interval_in_minutes: int = 0, days_to_run: List[str] = WEEK_DAYS) -> None:
        self.interval_in_seconds = datetime.timedelta(seconds=interval_in_seconds)
        self.interval_in_minutes = datetime.timedelta(minutes=interval_in_minutes)
        self.days_to_run = days_to_run
        self.last_run_dt = None

        T = time_interval[0]
        self.start_time = datetime.time.min if T == 'min' else datetime.time(*[int(x) for x in T.split(':')])
        T = time_interval[1]
        self.end_time = datetime.time.max if T == 'max' else datetime.time(*[int(x) for x in T.split(':')])

    def get_next_run_datetime(self):
        if self.last_run_dt is None:
            self.last_run_dt = datetime.datetime.now()

        next_run = self.last_run_dt + self.interval_in_minutes + self.interval_in_seconds

        while not self.is_day_legal(next_run):
            next_run = datetime.datetime(next_run.year, next_run.month, next_run.day) + datetime.timedelta(days=1)

        self.last_run_dt = next_run

        return next_run

    def is_day_legal(self, dt):
        return WEEK_DAYS[dt.weekday()] in self.days_to_run

    def cap_to_time_interval(self, time: datetime.time):
        if time < self.start_time:
            return self.start_time

        if time > self.end_time:
            return self.end_time

        return time
