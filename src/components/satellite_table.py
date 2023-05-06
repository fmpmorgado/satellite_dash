from dash import Dash, Input, Output, State, dash_table, html
import pandas as pd
from backend.satellite_data import request_data_from_source, request_data_from_id
from sgp4 import exporter
from collections import defaultdict

def render(app: Dash()):
    #Alternatively, import from Mongo
    list_satellites = request_data_from_source()

    #Preprocess data to store
    d = defaultdict(list)

    for sat in list_satellites:
        data = exporter.export_omm(sat,'ISS (ZARYA)')
        for key,value in data.items():
            d[key]+=[value]

    df = pd.DataFrame(d)

   # df.drop(columns=['CENTER_NAME', 'REF_FRAME', 'TIME_SYSTEM', 'MEAN_ELEMENT_THEORY' ])

    table = dash_table.DataTable(id = 'table_sat',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_cell={
            'textAlign': 'left',
            'height': 'auto',
            # all three widths are needed
            'minWidth': '180px', 'width': '180px', 'maxWidth': '300px',
            'whiteSpace': 'normal'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        },
        style_table={'overflowX': 'auto'},
        selected_rows=[],
        row_selectable="multi",
        sort_action="native",
        sort_mode="multi",
        page_size=20,  
    )

    @app.callback(Output('table_sat', 'active_cell'), Input('table_sat', 'active_cell'))
    def remove_active_cell(active_cell):
        return None

    @app.callback(Output('memory-satellite','data'),
                  Input('table_sat', 'selected_rows'),
                  State('table_sat', 'data'),
                  prevent_initial_call=True)
    def save_data_in_memory(rows,data):
        filtered = []
        for r in rows:
            name, tle1, tle2 = request_data_from_id(data[r]["NORAD_CAT_ID"])
            filtered += [{'name': name, 'tle1':tle1, 'tle2':tle2}]

        return filtered

    return html.Div(
            table,
        )