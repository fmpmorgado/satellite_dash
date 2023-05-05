import json
import os
import plotly.graph_objs as go


def trace():
    #Read json data of Earth
    #"https://raw.githubusercontent.com/Nov05/playground-fireball/master/data/earth.json"

    json_file = open(os.path.dirname(os.path.dirname(__file__))+"/data/earth.json")
    json_data = json.loads(json_file.read())

    #Parallel lines
    parallel = {}
    parallel['x'] = json_data['data'][0]['x']
    parallel['y'] = json_data['data'][0]['y']
    parallel['z'] = json_data['data'][0]['z']

    #Meridian lines
    meridian = {}
    meridian['x'] = json_data['data'][1]['x']
    meridian['y'] = json_data['data'][1]['y']
    meridian['z'] = json_data['data'][1]['z']

    #Earth base (dots)
    base = {}
    base['x'] = json_data['data'][2]['x']
    base['y'] = json_data['data'][2]['y']
    base['z'] = json_data['data'][2]['z']


    #Continents (lines)
    continent = {}
    continent['x'] = json_data['data'][3]['x']
    continent['y'] = json_data['data'][3]['y']
    continent['z'] = json_data['data'][3]['z']

    #Define colors
    color_lines = 'darkblue' # Parallels and Meridians
    color_base = 'darkblue'
    color_land = 'whitesmoke'
    opacity_base = 0.1
    opacity_land = 1.0
    width_land = 2.0
    size_lines = 1


    # Trace Parallels
    trace0 = go.Scatter3d( 
        x=parallel['x'], 
        y=parallel['y'], 
        z=parallel['z'], 
        mode='lines',
        marker=dict(
            size=size_lines,
            color=color_lines,
            opacity=opacity_base,
            showscale=False,
            line=dict(
                width=size_lines, 
                color=color_base)
            ),
        showlegend=False,
        hoverinfo="skip",
        name='Parallel'
        )


    # Trace Meridians
    trace1 = go.Scatter3d(
        x=meridian['x'],
        y=meridian['y'],
        z=meridian['z'],
        mode='lines',
        marker=dict(
            size=size_lines,
            color=color_lines,  
            opacity=opacity_base,
            showscale=False,
            line=dict(
                width=size_lines, 
                color=color_base,)
            ),
        showlegend=False,
        hoverinfo="skip",
        name='Meridian'
        )


    # Trace base surface (dots)
    trace2 = go.Scatter3d(
        x=base['x'],
        y=base['y'],
        z=base['z'],
        mode='markers',
        marker=dict(
            size=2,
            color=color_base,  
            opacity=opacity_base,
            showscale=False,
            line=dict(width=1, color=color_base)
            ),
        showlegend=False,
        hoverinfo="skip",
        name="base",
        )

    # land
    trace3 = go.Scatter3d(
        x=continent['x'],
        y=continent['y'],
        z=continent['z'],
        mode='lines',
        marker=dict(
            size=1,
            color=color_land,  
            opacity=opacity_land,
            showscale=False,
            ),
        line=dict(width=width_land, color=color_land),
        showlegend=False,
        hoverinfo="skip",
        name='land'
        )

    data = [trace0, trace1, trace2, trace3]

    return data