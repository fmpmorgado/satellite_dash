from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.routes import post_satellite, fetch_all_satellite
from backend.satellite_data import request_data_from_source, initialize_satellite_from_tle
from sgp4.exporter import export_omm
from backend.model import Satellite
import sys
import requests
import json

def print_output():
    sys.stdout.flush()

def update_database():
    names, tle_lines_1, tle_lines_2 = request_data_from_source()

    for name, tle1, tle2 in zip(names, tle_lines_1, tle_lines_2):
        sat = initialize_satellite_from_tle(tle1, tle2)
        fields = export_omm(sat, name)

        sat_entry = {"_id": fields["NORAD_CAT_ID"],
                                 "name": fields["OBJECT_NAME"].rstrip(),
                                 "tle1": tle1,
                                 "tle2": tle2,
                                 "epoch_tle": fields["EPOCH"]}

        #TODO change url for a dynamic url
        response = requests.post('http://127.0.0.1:8000/satellites', json=sat_entry)
        
    pass

@asynccontextmanager
async def init_scheduler(app: FastAPI):
    """
    Create a scheduler to update the Database with the new TLE data
    """

    print("Initializing application")
    
    #Updates the database after initializing the app
    #update_database()

    schedule = BackgroundScheduler()
    schedule.add_job(print_output, 'cron', second='*/1')
    schedule.add_job(update_database, 'cron', hour = '*/12')
    schedule.start()

    yield
    schedule.shutdown()