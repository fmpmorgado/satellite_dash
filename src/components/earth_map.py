import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from src import satellite
from backend.satellite_data import compute_position,initialize_satellite_from_tle
from datetime import datetime

def render(app = Dash()):

    @app.callback(Output('earth_map', 'figure'),
        Input('memory-satellite', 'data'),
        Input('interval1', 'n_intervals'),
        State('earth_map', 'figure'),
        prevent_initial_call=True)
    def update_earth_map(data, n, figure):        
        trace = []
        for sat in data:
            tle1 = sat["tle1"]
            tle2 = sat["tle2"]
            name = sat["name"]
            f = initialize_satellite_from_tle(tle1, tle2)
            lat, lon, __ = compute_position(datetime.now(), f)
            trace += [satellite.trace(lat=lat[0], lon=lon[0], satellite=f, name=name)]
        if trace:
            return go.Figure(data=trace, layout=figure['layout'])
        else:
            return figure
        
    layout = go.Layout(mapbox={"style": "open-street-map"}, 
                       margin={"r":0,"t":0,"l":0,"b":0})
    
    fig = go.Figure(data=[satellite.trace()], layout=layout)

    return html.Div(
        children = [
            dcc.Graph(id = "earth_map", figure=fig)
        ]
    )

    return fig