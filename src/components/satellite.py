import plotly.graph_objs as go

def trace():
    #Define properties
    size_marker = 0.5
    color_marker = 'white'
    opacity_base = 1.0

    # Trace satellite
    trace = go.Scatter3d( 
        x=[10000], 
        y=[10000],
        z=[10000], 
        mode='markers',
        marker=dict(
            size=size_marker,
            color=color_marker,
            opacity=opacity_base,
            showscale=False,
            line=dict(width=1, color=color_marker)
            ),
        showlegend=False,
        name='Satellite',
        )
    
    data = [trace]

    return data