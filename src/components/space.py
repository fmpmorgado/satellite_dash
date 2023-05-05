from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import earth
from . import satellite
import plotly.graph_objs as go

def render(app = Dash()):

    #Define colors
    color_background = 'black'

    #Retrieve data
    data_earth = earth.trace()
    data_satellite = satellite.trace()

    #Create the layout to render the images
    layout = go.Layout(
        autosize=True,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        ),
        scene=dict(xaxis=dict(title="x axis",
                            color=color_background,
                            backgroundcolor=color_background,
                            showaxeslabels=False,
                            showline=False,
                            showgrid=False,
                            zeroline=False,
                            ),
                yaxis=dict(title="y axis",
                            color=color_background,
                            backgroundcolor=color_background,
                            showaxeslabels=False,
                            showline=False,
                            showgrid=False,
                            zeroline=False,
                            ),
                zaxis=dict(title="z axis",
                            color=color_background,
                            backgroundcolor=color_background,
                            showaxeslabels=False,
                            showline=False,
                            showgrid=False,
                            zeroline=False,
                            ),
                ),
        paper_bgcolor=color_background,
        plot_bgcolor=color_background,
    )

    #Plot the data
    fig = go.Figure(data=data_earth+data_satellite, layout=layout)

    return html.Div(
        children = [
            dcc.Graph(id = "space_graph", figure=fig)
         #   dcc.Interval(id='interval1', interval=1 * 1000, n_intervals=0),
        ]
    )

