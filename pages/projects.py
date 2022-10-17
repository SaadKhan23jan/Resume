import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from .side_bar import sidebar

# This order means the order in which the page will be shown
dash.register_page(__name__, order=1)
layout = html.Div([
    dbc.Row(
        [
            dbc.Col([
                sidebar()
            ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2, ),
        ],
    )
])