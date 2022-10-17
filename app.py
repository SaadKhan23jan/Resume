import dash
import os
from dash import Dash, DiskcacheManager, CeleryManager
import dash_bootstrap_components as dbc

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)

else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__, background_callback_manager=background_callback_manager, use_pages=True, external_stylesheets=[dbc.themes.SUPERHERO])
app.title = 'Saad Khan Portfolio'

header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row([
                dbc.NavbarToggler(id="nav-bar_toggler"),
                dbc.Nav([
                    dbc.NavLink(page["name"], href=page["path"])
                    for page in dash.page_registry.values()
                    if not page["path"].startswith("/app")
                ])
            ])
        ],
        fluid=True
    ),
    dark=True,
    color='dark'
)

app.layout = dbc.Container([header, dash.page_container], fluid=False)

if __name__ == '__main__':
    app.run_server(debug=True)