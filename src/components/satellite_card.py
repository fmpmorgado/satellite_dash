import dash_bootstrap_components as dbc
from dash import html, Dash, Input, Output, State
from backend.satellite_data import compute_position, initialize_satellite_from_tle, compute_ECI_position
from datetime import datetime
import numpy as np
from sgp4 import exporter

def create_card_header(name, tle_line_1, tle_line_2):
    f = initialize_satellite_from_tle(tle_line_1, tle_line_2)
    field = exporter.export_omm(f,name)
    return [name, " | ", f"NORAD-ID: {field['NORAD_CAT_ID']}", " | ", f"INT-ID: {field['OBJECT_ID']}"]

def create_card_body_left(name, tle_line_1, tle_line_2):
    f = initialize_satellite_from_tle(tle_line_1, tle_line_2)
    lat, lon, alt = compute_position(datetime.now(), f)
    e, r, v = compute_ECI_position(datetime.now(), f)
    field = exporter.export_omm(f,name)

    return html.P([f"Latitude:  {round(lat[0],3)} deg", html.Br(),
                                    f"Longitude: {round(lon[0],3)} deg", html.Br(),
                                    f"Altitude:  {round(alt[0]/1000,1)} km", html.Br(),
                                    f"Speed: {round(np.linalg.norm(v),1)} km/s"])

def render(app: Dash()):

    @app.callback(Output('satellite_card_header', 'children'),
        Input('earth_map', 'clickData'),
        State('satellite_card_header', 'children'))
    def update_header(data, header):
        if not data:
            return header
        return create_card_header(data["points"][0]["customdata"][0], data["points"][0]["customdata"][1], data["points"][0]["customdata"][2])

    @app.callback(Output('satellite_card_body_left', 'children'),
        Output('satellite_card_body_right', 'children'),
        Input('earth_map', 'clickData'),
        Input('interval1','n_intervals'),
        State('satellite_card_body_left', 'children'),
        State('satellite_card_body_right', 'children'))
    def update_body(data, n, body_left, body_right):
        if not data and not body_left:
            return body_left, body_right
        
        b_left  = create_card_body_left(data["points"][0]["customdata"][0], data["points"][0]["customdata"][1], data["points"][0]["customdata"][2])

        return b_left, []

    card = dbc.Card(
        [
            dbc.CardHeader(children = html.H5(["Click over a satellite"], id = "satellite_card_header")),
            dbc.CardBody(
                [
                    dbc.Row([
                        dbc.Col([
                            html.P([], id = "satellite_card_body_left"),
                        ], width = 6),
                        dbc.Col([
                            html.P([], id = "satellite_card_body_right"),
                        ], width = 6)
                    ])
                ]
            ),
        ],
    )

    return html.Div(card,)