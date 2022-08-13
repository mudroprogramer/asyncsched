import asyncio
import logging
import pytest
from asyncsched.src.scheduler import RunLoop, RunOnce
from asyncsched.src.time_interval_core import TimeInterval

@pytest.mark.asyncio
async def test_run_once(capsys):
  
  async def coroutine():
    await asyncio.sleep(1)
    print("run")
    
  sched = RunOnce(coroutine, TimeInterval(interval_in_seconds=0))
  
  sched.start()
  
  print('test')
  
  await asyncio.sleep(1.1)
  
  captured = capsys.readouterr()
  assert captured.out == 'test\nrun\n'
  
@pytest.mark.asyncio
async def test_schedule_run(capsys, caplog):
  caplog.set_level(logging.INFO)
                   
  async def coroutine():
    print("run")
    
  sched = RunLoop(coroutine, TimeInterval(interval_in_seconds=1))
  
  sched.start()
  
  await asyncio.sleep(2.5)
  
  await sched.stop()

  captured = capsys.readouterr()
  assert captured.out == 'run\nrun\n'