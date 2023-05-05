import requests
import sgp4
from sgp4.api import Satrec, WGS72, jday
from sgp4 import exporter
import pymap3d as pm
from datetime import datetime

#http://celestrak.org/NORAD/elements/supplemental/sup-gp.php?SOURCE=SpaceX-E&FORMAT=CSV


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

for source in SOURCE[0:1]:

    url = f"http://celestrak.org/NORAD/elements/supplemental/sup-gp.php?SOURCE={source}&FORMAT={FORMAT}"
    res = requests.get(url)
    if res.ok:
        tle = res.text.replace('\r','').split('\n')[:3]

        name = tle[0]
        s = tle[1]
        t = tle[2]

        #s = "1 36411U 10008A   23125.19296515  .00000140  00000+0  00000+0 0  9998"
        #t = "2 36411   0.2538  95.3778 0001281 279.9331 133.7381  1.00141063 48228"

        #Default Earth model is WGS72
        #  Although WHS would be more accurate, according to https://pypi.org/project/sgp4/,
        #  the industry still uses WGS72
        satellite = Satrec.twoline2rv(s, t, WGS72)
        date = datetime.now()

        #jd: Julian Date and fr: fraction
        jd, fr = jday(date.year, date.month, date.day, date.hour, date.minute, date.second)

        #Compute position (km) and velocity(km/s) in TEME reference frame
        _, r, v = satellite.sgp4(jd, fr)

        lat,lon,alt = pm.eci2geodetic(r[0]*1000,r[1]*1000,r[2]*1000, t = date)


        print(lat,lon,alt)
        
        #Prints the data using Dataframe
        #print(exporter.export_omm(satellite, 'Test' ))