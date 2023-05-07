import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from backend import routes, scheduler

from dash import Dash
import dash_bootstrap_components as dbc
from src.components.layout import create_layout
import flask
import os

app = FastAPI(lifespan = scheduler.init_scheduler)

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')

# Dash setup
dash_app = Dash(__name__, server = server, requests_pathname_prefix="/dash/", external_stylesheets=[dbc.themes.PULSE])
dash_app.layout = create_layout(dash_app)
app.mount("/dash", WSGIMiddleware(dash_app.server))

app.include_router(routes.route)

app.add_middleware(
	CORSMiddleware,
	allow_origins = ["*"],
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"],
	)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, debug=True)