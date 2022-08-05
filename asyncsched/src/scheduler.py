import asyncio
import datetime
from typing import Coroutine

from asyncsched.src.time_interval_core import TimeInterval


class RunOnce:
    def __init__(self, func: Coroutine, timer: 'TimeInterval') -> None:
        self.task = None
        self.func = func
        self.timer = timer

    async def wait_until(self, dt):
        # sleep until the specified datetime
        now = datetime.datetime.now()
        await asyncio.sleep((dt - now).total_seconds())

    async def schedule_run(self, dt):
        await self.wait_until(dt)
        if (self.run):
            self.task = asyncio.create_task(self.func())

    def start(self):
        self.run = True
        run_at = self.timer.get_next_run_datetime()
        asyncio.create_task(self.schedule_run(run_at))

    async def stop(self):
        self.run = False

        if self.task:
            await self.task


class RunLoop(RunOnce):

    async def run_on_schedule(self):
        self.run = True
        self.last_run_dt = datetime.datetime.now()

        while self.run:
            self.last_run_dt = self.timer.get_next_run_datetime()
            await self.schedule_run(self.last_run_dt)

    def start(self):
        asyncio.create_task(self.run_on_schedule())
