import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# This order means the order in which the page will be shown
dash.register_page(__name__, order=3)

green_text = {"color": "green"}


def layout():
    return dbc.Row([
        dbc.Col([
            dcc.Markdown("# Saad Khan", className="mt-3"),
            dcc.Markdown("## Data Analyst", className="mb-5"),
            dcc.Markdown("### Personal Info", style={"color": "Lightgreen"}),
            dcc.Markdown("Address", style=green_text),
            dcc.Markdown("Duisburg 47057, NRW, Germany"),
            dcc.Markdown("Phone Number", style=green_text),
            dcc.Markdown("+49-178-5076545"),
            dcc.Markdown("Email", style=green_text),
            dcc.Markdown("saadkhan23jan@gmail.com"),
            dbc.Button("LinkedIn", href="https://www.linkedin.com/in/saad-khan-167704163/", target="_blank",
                       style={'size': '200px'}, className='me-1'),
            dbc.Button("Github", href="https://github.com/SaadKhan23jan/", target="_blank",
                       style={'size': '200px', 'marginLeft': '20px'}, className='me-1'),
        ], width={'size': 6, 'offset': 2})
    ], justify='center')
