import asyncio
import datetime
from typing import Coroutine, List, Tuple

WEEK_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


class Scheduler:

    def __init__(self, time_interval: Tuple[str] = ('min', 'max'), interval_in_seconds: int = 0, interval_in_minutes: int = 0, days_to_run: List[str] = WEEK_DAYS) -> None:
        self.interval_in_seconds = datetime.timedelta(seconds=interval_in_seconds)
        self.interval_in_minutes = datetime.timedelta(minutes=interval_in_minutes)
        self.days_to_run = days_to_run
        self.last_run_dt = datetime.datetime.now()

        T = time_interval[0]
        self.start_time = datetime.time.min if T == 'min' else datetime.time(*[int(x) for x in T.split(':')])
        T = time_interval[1]
        self.end_time = datetime.time.max if T == 'max' else datetime.time(*[int(x) for x in T.split(':')])

        self.task = None

    async def wait_until(self, dt):
        # sleep until the specified datetime
        now = datetime.datetime.now()
        await asyncio.sleep((dt - now).total_seconds())

    async def run_at(self, dt, coro):
        await self.wait_until(dt)
        self.task = asyncio.create_task(coro())
        return await self.task

    def get_next_run_datetime(self):
        next_run = self.last_run_dt + self.interval_in_minutes + self.interval_in_seconds

        while not self.is_day_legal(next_run):
            next_run = datetime.datetime(next_run.year, next_run.month, next_run.day) + datetime.timedelta(days=1)

        return next_run

    def is_day_legal(self, dt):
        return WEEK_DAYS[dt.weekday()] in self.days_to_run

    def cap_to_time_interval(self, time: datetime.time):
        if time < self.start_time:
            return self.start_time

        if time > self.end_time:
            return self.end_time

        return time

    async def run_on_schedule(self, coroutine: Coroutine):
        while self.run:
            self.last_run_dt = self.get_next_run_datetime()
            await self.run_at(self.last_run_dt, coroutine)

    def start_async(self, coroutine: Coroutine):
        self.run = True
        self.last_run_dt = datetime.datetime.now()
        asyncio.create_task(self.run_on_schedule(coroutine))

    async def stop(self):
        await asyncio.sleep(0.1)
        self.run = False

        if self.task:
            await self.task
