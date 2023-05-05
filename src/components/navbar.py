import dash_bootstrap_components as dbc

def render():

    navbar = dbc.NavbarSimple(
        brand="Satellite Tracker",
        brand_href="#",
        color="primary",
        dark=True,
    )

    return navbar