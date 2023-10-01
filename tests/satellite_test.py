import os
import sys
import numpy as np
from datetime import datetime
import requests

# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

from backend.model import Satellite, string_to_date
from backend.satellite_data import SOURCE, FORMAT
from backend.satellite_data import initialize_satellite_from_tle, compute_ECI_position, compute_position

sat_entry = {"_id": "Test",
             "name": "Test satellite",
             "tle1": "1 01328C 65032A   23272.98750000  .00000013  00000+0  20745-4 0  2724",
             "tle2": "2 01328  41.1841 298.0729 0252630 191.2215 123.1720 13.38753621    17",
             "epoch_tle": "2023-09-29T23:42:00.000000"}

def test_requests():
    """
    Test request of the different satellite sources for celestrak
    """
    
    for source in SOURCE:

        url = f"http://celestrak.org/NORAD/elements/supplemental/sup-gp.php?SOURCE={source}&FORMAT={FORMAT}"
        res = requests.get(url)
        if res.ok:
            pass
        else: assert False

def test_position():
    """
    Test computation of satellite position
    """

    satellite = initialize_satellite_from_tle(sat_entry["tle1"], sat_entry["tle2"])
    date = string_to_date(sat_entry["epoch_tle"])
    lat, lon, alt = compute_position(current_time=date, satellite=satellite)
    assert np.round(lat,5) == np.round(-26.957341,5)
    assert np.round(lon,5) == np.round(-101.237315,5)
    assert np.round(alt,5) == np.round(1227506.9849629,5)
