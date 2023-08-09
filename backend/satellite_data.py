import requests
from sgp4.api import Satrec, WGS72, jday
import pymap3d as pm
import numpy as np

"""
TLE sources to request from celestrak

"CPF (Consolidated Laser Ranging Predictions)"
"GLONASS-RE (GLONASS Rapid Ephemeris)
"GPS-A (GPS Almanac)
"GPS-E (GPS Ephemeris)
"Intelsat-11P (Intelsat 11-Parameter Data)
"Intelsat-E (Intelsat Epehemeris)
"Iridium-E (Iridium Ephemeris)
"ISS-E (ISS Ephemeris)
"ISS-TLE (ISS TLE [legacy data])
"METEOSAT-SV (METEOSAT State Vector)
"OneWeb-E (OneWeb Ephemeris)
"Orbcomm-TLE (Orbcomm-Provided SupTLE)
"Planet-E (Planet Ephemeris)
"SES-11P (SES 11-Parameter Data)
"SpaceX-E (SpaceX Ephemeris)
"SpaceX-SV (SpaceX State Vector)
"Telesat-E (Telesat Ephemeris)
"Transporter-SV (Transporter State Vectors)
"""

SOURCE = ["CPF", "GLONASS-RE", "GPS-A", "GPS-E", "Intelsat-11P", "Intelsat-11P", "Intelsat-E", "Iridium-E", "ISS-E", "ISS-TLE", "METEOSAT-SV", "OneWeb-E", "Orbcomm-TLE", "Planet-E", "SES-11P", "SpaceX-E", "SpaceX-SV", "Telesat-E", "Transporter-SV"]
FORMAT = "TLE"

def request_data_from_source():

    names= []
    tle_line_1 = []
    tle_line_2 = []

    for source in SOURCE:

        url = f"http://celestrak.org/NORAD/elements/supplemental/sup-gp.php?SOURCE={source}&FORMAT={FORMAT}"
        res = requests.get(url)
        if res.ok:
            tle = res.text.replace('\r','').split('\n')

        #Collect TLE data
        names += tle[0::3]
        tle_line_1 += tle[1::3]
        tle_line_2 += tle[2::3]

    return names, tle_line_1, tle_line_2

def request_data_from_id(sat_id):

    names= ""
    tle_line_1 = ""
    tle_line_2 = ""

    url = f"http://celestrak.org/NORAD/elements/supplemental/sup-gp.php?CATNR={sat_id}&FORMAT={FORMAT}"
    res = requests.get(url)
    if res.ok:
        tle = res.text.replace('\r','').split('\n')

    names += tle[0]
    tle_line_1 += tle[1]
    tle_line_2 += tle[2]
    
    return names.rstrip(), tle_line_1, tle_line_2

def initialize_satellite_from_tle(tle_line_1, tle_line_2):
    
    #Default Earth model is WGS72
    #  Although WHS would be more accurate, according to https://pypi.org/project/sgp4/,
    #  the industry still uses WGS72

    return Satrec.twoline2rv(tle_line_1, tle_line_2, WGS72)

def compute_ECI_position(current_time, satellite):
    date = current_time

    #jd: Julian Date and fr: fraction
    jd, fr = jday(date.year, date.month, date.day, date.hour, date.minute, date.second)

    #Compute position (km) and velocity(km/s) in TEME reference frame
    e, r, v = satellite.sgp4(jd, fr)

    return e,r,v

def compute_position(current_time, satellite):
    date = current_time

    e, r, v = compute_ECI_position(date, satellite)

    #Compute x,y,z positions
    x,y,z = pm.eci2ecef(r[0]*1000,r[1]*1000,r[2]*1000, time = date)

    #Compute latitude, longitude and altitude
    lat,lon,alt = pm.eci2geodetic(r[0]*1000,r[1]*1000,r[2]*1000, t = date)

    return lat, lon, alt


def compute_ECI_position_array(time_array, satellite):

    jd = ()
    fr = ()

    for date in time_array:
        a, b = jday(date.year, date.month, date.day, date.hour, date.minute, date.second)
        jd += (a,)
        fr += (b,)

    jd = np.array(jd)
    fr = np.array(fr)

    #Compute position (km) and velocity(km/s) in TEME reference frame
    e, r, v = satellite.sgp4_array(jd, fr)

    return e,r,v

def compute_position_array(time_array, satellite):
    
    e, r, v = compute_ECI_position_array(time_array, satellite)

    #Compute latitude, longitude and altitude
    lat,lon,alt = pm.eci2geodetic(r[:,0]*1000,r[:,1]*1000,r[:,2]*1000, t = time_array)

    return lat, lon, alt    