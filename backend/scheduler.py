from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import os
import sys

def check_list_len():
    print("Teste")
    sys.stdout.flush()

@asynccontextmanager
async def init_scheduler(app: FastAPI):
    """
    Create a scheduler to update the Database with the new TLE data
    """

    schedule = BackgroundScheduler()
    schedule.add_job(check_list_len, 'cron', second='*/1')
    schedule.start()
    yield
    schedule.shutdown()