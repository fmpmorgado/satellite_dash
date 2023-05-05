from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from src.components import earth
from src.components.layout import create_layout

# Dash setup
app = Dash(__name__,external_stylesheets=[dbc.themes.PULSE])
server = app.server

app.layout = create_layout(app)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)

