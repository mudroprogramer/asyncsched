import asyncio
import datetime
from typing import Coroutine

from asyncsched.src.time_interval_core import TimeInterval


class RunOnce:
    def __init__(self, func: Coroutine, timer: 'TimeInterval') -> None:
        self.task = None
        self.func = func
        self.timer = timer

    async def schedule_run(self, seconds):
        await asyncio.sleep(seconds)
        if (self.run):
            self.task = asyncio.create_task(self.func())

    def start(self):
        self.run = True
        seconds_to_sleep = self.timer.seconds_to_next_run()
        asyncio.create_task(self.schedule_run(seconds_to_sleep))

    async def stop(self):
        self.run = False

        if self.task:
            await self.task


class RunLoop(RunOnce):

    async def run_on_schedule(self):
        self.run = True

        while self.run:
            seconds_to_sleep = self.timer.seconds_to_next_run()
            await self.schedule_run(seconds_to_sleep)

    def start(self):
        asyncio.create_task(self.run_on_schedule())
