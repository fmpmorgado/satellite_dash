import plotly.graph_objs as go
from sgp4 import exporter
import numpy as np

#Pass satellite data
def position_trace(lat = 0, lon = 0, satellite = None, name = "skip"):

    if satellite == None:
        return go.Scattermapbox(lat=[lat], lon=[lon], mode="markers", marker= {'size': 0}, name=name)

    #Check TLE
    line1, line2 = exporter.export_tle(satellite)
    fields = exporter.export_omm(satellite, name)

    #Define properties
    size_marker = 10
    color_marker = "black"
    opacity = 0.7

    # Trace satellite
    trace = go.Scattermapbox(lat=[round(lat,3)],
                            lon=[round(lon,3)],
                            hoverinfo="text+lon+lat",
                            text = name,
                            mode="markers",
                            marker= {'size': size_marker, 'symbol':"circle", 'color':color_marker, 'opacity': opacity},
                            customdata=[[fields["OBJECT_NAME"], line1, line2]],
                           # hovertemplate=
                           #   "TLE1:%{customdata[0]}",
                            name = fields["OBJECT_NAME"],
                            showlegend=False,
                            )
    data = [trace]

    return trace

def orbit_trace(lat, lon):
    
    #Add NaN when lat or lon change sign
    index = 1
    lat = list(lat)
    lon = list(lon)

    while index != len(lat):
        if np.sign(lon[index-1])!= np.sign(lon[index]):
            lat.insert(index, None)
            lon.insert(index, None)
            index +=1
        index += 1


    #Define properties
    size_line = 2
    color_line = "red"
    opacity = 0.7

    # Trace satellite
    trace = go.Scattermapbox(lat=lat,
                            lon=lon,
                            hoverinfo="skip",
                            name = "orbit",
                            mode="lines",
                            line= {'width': size_line, 'color': color_line},
                            showlegend=False,
                            )
    
    return trace
