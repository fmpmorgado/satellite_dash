import plotly.graph_objs as go
from sgp4 import exporter

#Pass satellite data
def trace(lat = 0, lon = 0, satellite = None, name = "skip"):

    if satellite == None:
        return go.Scattermapbox(lat=[lat], lon=[lon], mode="markers", marker= {'size': 0}, name=name)

    #Check TLE
    line1, line2 = exporter.export_tle(satellite)
    fields = exporter.export_omm(satellite, name)

    #Define properties
    size_marker = 10
    color_marker = 'white'
    opacity_base = 1.0

    # Trace satellite
    trace = go.Scattermapbox(lat=[round(lat,3)],
                            lon=[round(lon,3)],
                            hoverinfo="text+lon+lat",
                            text = name,
                            mode="markers",
                            marker= {'size': size_marker},
                            customdata=[[fields["OBJECT_NAME"], line1, line2]],
                           # hovertemplate=
                           #   "TLE1:%{customdata[0]}",
                            name = fields["OBJECT_NAME"],
                            showlegend=False,
                            )
    data = [trace]

    return trace