import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from src import satellite
from backend.satellite_data import compute_position, initialize_satellite_from_tle, compute_position_array
from datetime import datetime, timedelta
from sgp4 import exporter

def render(app = Dash()):

    @app.callback(Output('earth_map', 'figure'),
        Input('memory-satellite', 'data'),
        Input('interval1', 'n_intervals'),
        Input('earth_map', 'clickData'),
        State('earth_map', 'figure'),
        prevent_initial_call=True)
    def update_earth_map(data, n, clickdata, figure):        
        trace = []
        if not data: return figure

        #Loop the data in memory that was selected in the table
        for sat in data:
            tle1 = sat["tle1"]
            tle2 = sat["tle2"]
            name = sat["name"]
            f = initialize_satellite_from_tle(tle1, tle2)
            lat, lon, __ = compute_position(datetime.now(), f)
            trace += [satellite.position_trace(lat=lat[0], lon=lon[0], satellite=f, name=name)]
        
        if clickdata:
            name = clickdata["points"][0]["customdata"][0]
            tle1 = clickdata["points"][0]["customdata"][1]
            tle2 = clickdata["points"][0]["customdata"][2]
            f = initialize_satellite_from_tle(tle1, tle2)

            #From the satellite information, retrieve the Period
            T = 1/float(exporter.export_omm(f, '')["MEAN_MOTION"])*24*60

            #Create list of timestamps to create the orbit, in relation to the period value
            base = datetime.now()
            date_list = [base + timedelta(minutes=x) for x in range(int(T))]

            #compute the array of latitude and longitude
            lat, lon, __ = compute_position_array(date_list, f)

            #Create the trace of the orbit
            trace += [satellite.orbit_trace(lat = lat, lon = lon)]


        #Check if last trace corresponds to an orbit
        elif figure["data"][-1]["name"] == "orbit":
            trace+=figure["data"][-1]
        
        if trace:
            return go.Figure(data=trace, layout=figure['layout'])
        else:
            return figure
        
    layout = go.Layout(mapbox={"style": "open-street-map"}, 
                       margin={"r":0,"t":0,"l":0,"b":0})
    
    fig = go.Figure(data=[satellite.position_trace()], layout=layout)

    return html.Div(
        children = [
            dcc.Graph(id = "earth_map", figure=fig)
        ]
    )