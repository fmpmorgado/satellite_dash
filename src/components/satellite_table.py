from dash import Dash, Input, Output, State, dash_table, html
import pandas as pd
from backend.satellite_data import request_data_from_source, request_data_from_id, initialize_satellite_from_tle
from sgp4 import exporter
from collections import defaultdict

def render(app: Dash()):
    #Alternatively, import from Mongo
    names, tle_lines_1, tle_lines_2= request_data_from_source()
    list_satellites = [initialize_satellite_from_tle(tle1, tle2) for tle1, tle2 in zip(tle_lines_1, tle_lines_2)]
    #Preprocess data to store
    d = defaultdict(list)

    for sat, name in zip(list_satellites, names):
        data = exporter.export_omm(sat, name)
        for key,value in data.items():
            d[key]+=[value]

    df = pd.DataFrame(d)

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
        filter_action='native',
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