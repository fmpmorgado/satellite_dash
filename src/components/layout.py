from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date, datetime, timedelta
from . import space
from . import navbar

import pandas as pd

#https://gitlab.com/librespacefoundation/python-satellitetle/-/tree/master/satellite_tle

df = pd.DataFrame(
    {
        "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"]*2,
        "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"]*2,
    }
)

table = dbc.Table.from_dataframe(df, id = "table", striped=True, bordered=True, hover=True)

def create_layout(app = Dash()):

    @app.callback(Output('label1', 'children'),
        [Input('interval1', 'n_intervals')])
    def update_interval(n):
        return 'Time: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
   # @app.callback(
   #         Output('table','children'),
   #         [Input('interval1', 'n_intervals')])
    def update_table(n_click):
        df = pd.DataFrame(
        {
            "First Name": ["Ar", "Ford", "Zaphod", "Trillian"],
            "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
        }
        )
        
        return dbc.Table.from_dataframe(df)


    return  dbc.Container([
                dbc.Row([navbar.render()]),
                dbc.Row([
                    dbc.Col([
                        html.H6(id='label1', children='', style={'textAlign':'center'}),
                        space.render(app),
                        table,
                        dcc.Interval(id='interval1', interval=1 * 1000, n_intervals=0),
                        ],
                        width = 6
                    )
                ])
            ], fluid = True)
