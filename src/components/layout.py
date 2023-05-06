from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime
from . import earth_map, navbar, satellite_table, satellite_card

def create_layout(app = Dash()):

    @app.callback(Output('label1', 'children'),
        [Input('interval1', 'n_intervals')])
    def update_interval(n):
        return 'Time UTC: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return  dbc.Container([
                dbc.Row([navbar.render()]),
                dbc.Row([
                    dbc.Col([
                        html.H6(id='label1', children='', style={'textAlign':'center'}),
                        earth_map.render(app),
                        satellite_card.render(app),
                        dcc.Interval(id='interval1', interval=1 * 1000, n_intervals=0),
                        ],
                        width = 6
                    ),
                    dcc.Store(id='memory-satellite'),
                    dbc.Col([satellite_table.render(app)],
                        width = 6)
                ])
            ], fluid = True)
