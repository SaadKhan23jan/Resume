from datetime import datetime as dt
import os
import dash
import dash_bootstrap_components as dbc
from dateutil.relativedelta import relativedelta
from dash import html, dcc, DiskcacheManager, CeleryManager, callback
from dash.dependencies import Input, Output, State
import yfinance as yf
from stock_list import crypto_list
from market_functions import sarimax_pred, crypto_plots, decomposition

import warnings
warnings.filterwarnings("ignore")

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

dash.register_page(__name__)

layout = html.Div([
    html.Div(
        html.H1("Welcome to Live Crypto/Stock Market Data and Predictions",
                style={'color': 'black', 'textAlign': 'center', 'backgroundColor': 'Lightgreen'})
    ),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Label('Select Crypto-Pair/Stock Market', style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='crypto-pair', options=crypto_list,
                             style={'color': 'black', 'width': '100%'}, value='BTC-USD'),
            ]),
        ]),

        dbc.Col([
            html.Div([
                html.Label('Select Time Frame', style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='time-frame', options=[{'label': '10 Year', 'value': '10y'},
                                                       {'label': '1 Year', 'value': '1y'},
                                                       {'label': '6 Months', 'value': '6mo'},
                                                       {'label': '3 Months', 'value': '3mo'},
                                                       {'label': '1 Months', 'value': '1mo'},
                                                       {'label': '1 Week', 'value': '1wk'},
                                                       {'label': '1 Day', 'value': '24h'}],
                             style={'color': 'black', 'width': '100%'}, value='1y'),
            ]),
        ]),

    ]),


    html.Div(
        dcc.Graph(id='graph-candlestick')
    ),

    html.Div(
        dcc.Graph(id='graph-line'),
    ),

    html.Div(
        dcc.Graph(id='decomposed-graphs')
    ),

    html.Div(
        dcc.Graph(id='volume-graph-line')
    ),

    html.Div([
        html.H2("SARIMAX Models Predictions"),
        html.Br(),

        html.Label('Select one of SARIMAX Model:   '),
        dcc.Dropdown(id='sarimax-model', options=[{'label': 'MA', 'value': 'MA'},
                                                  {'label': 'AR', 'value': 'AR'},
                                                  {'label': 'ARMA', 'value': 'ARMA'},
                                                  {'label': 'ARIMA', 'value': 'ARIMA'},
                                                  {'label': 'SARIMAX', 'value': 'SARIMAX'},
                                                  {'label': 'Auto ARIMA', 'value': 'Auto ARIMA'}
                                                  ],
                     style={'color': 'black', 'width': '50%'},
                     value='ARIMA'
                     ),
        html.Br(),

        html.Div(
            id='auto-arima-container',
            children=html.Div([
                html.Div([
                    html.Div([
                        html.Label('Starting value of p:', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Input(id='start-p-order', type='number', value=0, inputMode='numeric', min=0, )
                    ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                              'paddingRight': '10px', 'paddingTop': '15px'},
                    ),

                    html.Div([
                        html.Label('Starting value of i:', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Input(id='start-i-order', type='number', value=0, inputMode='numeric', min=0)
                    ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                              'paddingRight': '10px', 'paddingTop': '15px'},
                    ),

                    html.Div([
                        html.Label('Starting value of q:', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Input(id='start-q-order', type='number', value=0, inputMode='numeric', min=0)
                    ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                              'paddingRight': '10px', 'paddingTop': '15px'},
                    ),
                    html.Div([
                        html.Label('Maximum value of p:', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Input(id='max-p-order', type='number', value=1, inputMode='numeric', min=1),
                        html.Div(id='error-max-p', children=[]),
                    ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                              'paddingRight': '10px', 'paddingTop': '15px'},
                    ),

                    html.Div([
                        html.Label('Maximum value of i:', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Input(id='max-i-order', type='number', value=1, inputMode='numeric', min=1),
                        html.Div(id='error-max-i'),
                    ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                              'paddingRight': '10px', 'paddingTop': '15px'},
                    ),

                    html.Div([
                        html.Label('Maximum value of q:', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Input(id='max-q-order', type='number', value=1, inputMode='numeric', min=1),
                        html.Div(id='error-max-q'),
                    ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                              'paddingRight': '10px', 'paddingTop': '15px'},
                    ),

                ], style={'color': 'black', 'display': 'flex'}),
                html.Br(),
                html.Div([
                    html.Div([

                        html.Label('Select the Seasonal Factor', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Dropdown(id='auto-arima-seasonal-factor',
                                     options=[{'label': 'Quarterly', 'value': 3},
                                              {'label': '4-Monthly', 'value': 4},
                                              {'label': 'Bi-Yearly', 'value': 6},
                                              {'label': 'Yearly', 'value': 12}, ],
                                     value=12),
                    ], style={'color': 'black', 'width': '300px', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px',
                              'marginLeft': '10px', 'paddingRight': '10px', 'paddingTop': '15px'}, hidden=False),

                    html.Div([
                        html.Label('Seasonal', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Dropdown(id='auto-arima-seasonal',
                                     options=[{'label': 'True', 'value': 'True'},
                                              {'label': 'False', 'value': 'False'}, ],
                                     value='False'),
                    ], style={'color': 'black', 'width': '300px', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px',
                              'marginLeft': '10px', 'paddingRight': '10px', 'paddingTop': '15px'},),
                    html.Div([
                        html.Label('Stationary', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Dropdown(id='auto-arima-stationary',
                                     options=[{'label': 'True', 'value': 'True'},
                                              {'label': 'False', 'value': 'False'}, ],
                                     value='False'),
                    ], style={'color': 'black', 'width': '300px', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px',
                              'marginLeft': '10px', 'paddingRight': '10px', 'paddingTop': '15px'},),

                    html.Div([
                        html.Label('Information Criteria', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Dropdown(id='auto-arima-information-criterion',
                                     options=[{'label': 'AIC', 'value': 'aic'},
                                              {'label': 'BIC', 'value': 'bic'},
                                              {'label': 'HQIC', 'value': 'hqic'},
                                              {'label': 'OOB', 'value': 'oob'}, ],
                                     value='aic'),
                    ], style={'color': 'black', 'width': '300px', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px',
                              'marginLeft': '10px', 'paddingRight': '10px', 'paddingTop': '15px'},),

                    html.Div([
                        html.Label('Method to be used', style={'color': 'black', 'paddingRight': '20px'}),
                        dcc.Dropdown(id='auto-arima-method',
                                     options=[{'label': 'Newton-Raphson', 'value': 'newton'},
                                              {'label': 'Nelder-Mead', 'value': 'nm'},
                                              {'label': ' Broyden-Fletcher-Goldfarb-Shanno (BFGS)', 'value': 'bfgs'},
                                              {'label': 'limited-memory BFGS with optional box constraints',
                                               'value': 'lbfgs'},
                                              {'label': 'modified Powell’s method', 'value': 'powell'},
                                              {'label': 'conjugate gradient', 'value': 'cg'},
                                              {'label': 'Newton-conjugate gradient', 'value': 'ncg'},
                                              {'label': 'global basin-hopping solver', 'value': 'basinhopping'}, ],
                                     value='lbfgs')
                    ], style={'color': 'black', 'width': '300px', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px',
                              'marginLeft': '10px', 'paddingRight': '10px', 'paddingTop': '15px'},)
                ], style={'display': 'flex'}),

            ]),
            hidden=True,
        ),

        html.Div(
            id='sarimax-container',
            children=html.Div([
                html.Div([
                    html.Label('Enter the order of P:', style={'color': 'black', 'paddingRight': '20px'}),
                    dcc.Input(id='sarimax-p-order', type='number', value=0, inputMode='numeric', min=0, )
                ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                          'paddingRight': '10px', 'paddingTop': '15px'},
                ),

                html.Div([
                    html.Label('Enter the order of I:', style={'color': 'black', 'paddingRight': '20px'}),
                    dcc.Input(id='sarimax-i-order', type='number', value=0, inputMode='numeric', min=0)
                ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                          'paddingRight': '10px', 'paddingTop': '15px'},
                ),

                html.Div([
                    html.Label('Enter the order of Q:', style={'color': 'black', 'paddingRight': '20px'}),
                    dcc.Input(id='sarimax-q-order', type='number', value=0, inputMode='numeric', min=0, )
                ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                          'paddingRight': '10px', 'paddingTop': '15px'},
                ),

                html.Div([
                    html.Label('Select the Seasonal Factor'),
                    dcc.Dropdown(id='seasonal-factor', options=[{'label': 'Quarterly', 'value': 3},
                                                                {'label': '4-Monthly', 'value': 4},
                                                                {'label': 'Bi-Yearly', 'value': 6},
                                                                {'label': 'Yearly', 'value': 12}, ],
                                 value=12),
                ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                          'paddingRight': '10px', 'paddingTop': '15px'}, hidden=False),

            ], style={'color': 'black', 'display': 'flex'}),
            hidden=True,
        ),

        html.Br(),
        html.Br(),

        html.Div([
            html.Div(
                id='p-order-container',
                children=[
                    html.Label('Enter the order of p:', style={'color': 'black', 'paddingRight': '20px'}),
                    dcc.Input(id='p-order', type='number', placeholder='Enter the order of P', value=0,
                              inputMode='numeric', min=0, required=True),
                ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                          'paddingRight': '10px', 'paddingTop': '15px'}, hidden=False,
            ),

            html.Div(
                id='i-order-container',
                children=[
                    html.Label('Enter the order of i:', style={'color': 'black', 'paddingRight': '20px'}),
                    dcc.Input(id='i-order', type='number', placeholder='Enter the order of I', value=0,
                              inputMode='numeric', min=0),
                ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                          'paddingRight': '10px', 'paddingTop': '15px'}, hidden=False,
            ),

            html.Div(
                id='q-order-container',
                children=[
                    html.Label('Enter the order of q:', style={'color': 'black', 'paddingRight': '20px'}),
                    dcc.Input(id='q-order', type='number', placeholder='Enter the order of Q', value=0,
                              inputMode='numeric', min=0),
                ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                          'paddingRight': '10px', 'paddingTop': '15px'}, hidden=False,
            ),
            html.Div([
                html.Label('Days for Forecast:', style={'color': 'black', 'paddingRight': '20px'}),
                dcc.Input(id='days', type='number', placeholder='Enter the order of Q', value=14,
                          inputMode='numeric', min=0,),
            ], style={'color': 'black', 'backgroundColor': '#f3f2f5', 'borderRadius': '10px', 'marginLeft': '10px',
                      'paddingRight': '10px', 'paddingTop': '15px'}, hidden=False
            ),

        ], style={'color': 'black', 'display': 'flex'}),

        html.Br(),

        html.Div([
            html.Div([html.P(id='run-calc', children=['Calculations are not yet Started'])]),
            html.Button(id='run-pred', children='Run Forecast',
                        style={'color': 'black', 'weight': 'bold', 'height': '100px', 'borderRadius': '30px', 'paddingRight': '20px',
                               'fontWeight': 'bold', 'fontSize': '20px'}),
            html.Button(id='stop-pred', children='Stop Forecast',
                        style={'color': 'black', 'weight': 'bold', 'height': '100px', 'borderRadius': '30px', 'paddingLeft': '20px',
                               'fontWeight': 'bold', 'fontSize': '20px'}),

        ]
        ),


        html.Br(),
        html.Br(),

        html.Div(id='sarimax-results'),

    ]),


    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        html.H1([f'Predictions Through ',
                 html.Label(id='model_used', style={'fontSize': '40px', 'color': 'blue', 'weight': 'bold'}),
                 ' Model']),

    ], style={'color': 'black', 'borderRadius': '20px', 'width': '800px',
              'backgroundColor': '#e6f5f4', 'padding': '30px'}),


    dcc.Graph(id='fig-pred'),

    html.P('***Note***: This is for demo purpose and the results are never claimed to be correct, nor can be used'
           ' for real time prediction of the actual data', style={'color': 'black', 'color': 'white', 'backgroundColor': 'black'}),



], style={'color': 'black', 'background-color': 'Lightgreen'})


@dash.callback(
    output=Output('run-calc', 'children'),
    inputs=Input('run-pred', 'n_clicks'),
    background=True,
    running=[
        (Output('run-pred', 'disabled'), True, False),
        (Output('stop-pred', 'disabled'), False, True),
    ],
    cancel=[Input('stop-pred', 'n_clicks')],
)
def run_calculations(n_clicks):
    # time.sleep(2.0)
    return [f"Click on Run to Start Calculations or Stop to Cancel the Calculations or Refresh the page"]


@callback([Output('error-max-p', 'children'),
           Output('error-max-i', 'children'),
           Output('error-max-q', 'children'), ],
          [Input('max-p-order', 'value'),
           Input('max-i-order', 'value'),
           Input('max-q-order', 'value'),
           Input('start-p-order', 'value'),
           Input('start-i-order', 'value'),
           Input('start-q-order', 'value'), ]
          )
def error_alert(max_p_order, max_i_order, max_q_order, start_p_order,  start_i_order,  start_q_order):

    # This code is short form, else it can be written in 6 lines of if-else statements
    alert_p, alert_i, alert_q, = ('', '', '')

    if max_p_order <= start_p_order:
        alert_p = 'Should be greater than Starting p value'
    if max_i_order <= start_i_order:
        alert_i = 'Should be greater than Starting i value'
    if max_q_order <= start_q_order:
        alert_q = 'Should be greater than Starting q value'

    return alert_p, alert_i, alert_q


@callback([Output('auto-arima-container', 'hidden'),
           Output('sarimax-container', 'hidden'),
           Output('p-order-container', 'hidden'),
           Output('i-order-container', 'hidden'),
           Output('q-order-container', 'hidden'), ],
          Input('sarimax-model', 'value'),
          prevent_initial_call=True)
def update_output(sarimax_model):
    if sarimax_model == 'SARIMAX':
        return True, False, False, False, False
    elif sarimax_model == 'MA':
        return True, True, True, True, False
    elif sarimax_model == 'AR':
        return True, True, False, True, True
    elif sarimax_model == 'ARMA':
        return True, True, False, True, False
    elif sarimax_model == 'ARIMA':
        return True, True, False, False, False
    elif sarimax_model == 'Auto ARIMA':
        return False, True, True, True, True
    else:
        return False, False, True, True, True


@callback([Output('graph-candlestick', 'figure'),
           Output('graph-line', 'figure'),
           Output('volume-graph-line', 'figure'),
           Output('decomposed-graphs', 'figure')],
          [Input('crypto-pair', 'value'),
           Input('time-frame', 'value'), ],
          )
def update_graph(crypto, time_frame):

    if time_frame in ['10y']:
        interval = '1mo'
        start = (dt.now()-relativedelta(years=10))
    elif time_frame in ['1y']:
        interval = '1mo'
        start = (dt.now() - relativedelta(years=1))
    elif time_frame in ['6mo']:
        interval = '5d'
        start = (dt.now() - relativedelta(months=6))
    elif time_frame in ['3mo']:
        interval = '1d'
        start = (dt.now() - relativedelta(months=3))
    elif time_frame in ['1mo']:
        interval = '90m'
        start = (dt.now() - relativedelta(months=1))
    elif time_frame in ['1wk']:
        interval = '30m'
        start = (dt.now() - relativedelta(weeks=1))
    elif time_frame in ['24h']:
        interval = '1m'
        start = (dt.now() - relativedelta(hours=1))
    else:
        interval = '1m'
        start = dt.now() - relativedelta(minutes=60)

    end = dt.now()

    df_live = yf.download(tickers=crypto, start=start, end=end, interval=interval)

    fig1, fig2, fig3 = crypto_plots(df_live, crypto)

    fig_seasonality_decompose = decomposition(df_live)

    return fig1, fig2, fig3, fig_seasonality_decompose


@callback([Output('sarimax-results', 'children'),
           Output('fig-pred', 'figure'),
           Output('model_used', 'children'), ],
          [Input('run-pred', 'n_clicks'),
           State('time-frame', 'value'),
           State('crypto-pair', 'value'),
           State('p-order', 'value'),
           State('i-order', 'value'),
           State('q-order', 'value'),
           State('sarimax-model', 'value'),
           State('days', 'value'),
           State('sarimax-p-order', 'value'),
           State('sarimax-i-order', 'value'),
           State('sarimax-q-order', 'value'),
           State('seasonal-factor', 'value'),
           State('start-p-order', 'value'),
           State('start-i-order', 'value'),
           State('start-q-order', 'value'),
           State('max-p-order', 'value'),
           State('max-i-order', 'value'),
           State('max-q-order', 'value'),
           State('auto-arima-seasonal-factor', 'value'),
           State('auto-arima-seasonal', 'value'),
           State('auto-arima-stationary', 'value'),
           State('auto-arima-information-criterion', 'value'),
           State('auto-arima-method', 'value'),
           ])
def predictions(n_clicks, time_frame, crypto, p, i, q, sarimax_model, days, sp, si, sq, seasonal_factor,
                start_p_order, start_i_order, start_q_order, max_p_order, max_i_order, max_q_order,
                auto_arima_seasonal_factor, auto_arima_seasonal, auto_arima_stationary,
                auto_arima_information_criterion, auto_arima_method):

    if time_frame == '10y':
        interval = '90m'
        start = (dt.now()-relativedelta(years=10))
    elif time_frame in ['1y']:
        interval = '1wk'
        start = (dt.now() - relativedelta(years=1))
    elif time_frame in ['6mo']:
        interval = '5d'
        start = (dt.now() - relativedelta(months=6))
    elif time_frame in ['3mo']:
        interval = '1d'
        start = (dt.now() - relativedelta(months=3))
    elif time_frame in ['1mo']:
        interval = '90m'
        start = (dt.now() - relativedelta(months=1))
    elif time_frame in ['1wk']:
        interval = '30m'
        start = (dt.now() - relativedelta(weeks=1))
    elif time_frame in ['24h']:
        interval = '1m'
        start = (dt.now() - relativedelta(hours=23))
    else:
        interval = '1m'
        start = dt.now() - relativedelta(days=1)

    end = dt.now()

    df_live = yf.download(tickers=crypto, start=start, end=end, interval=interval)

    # Here we will call our function for SARIMAX Model

    if auto_arima_seasonal == 'True':
        auto_arima_seasonal = True
    else:
        auto_arima_seasonal = False

    if auto_arima_stationary == 'True':
        auto_arima_stationary = True
    else:
        auto_arima_stationary = False

    results, pred_fig = sarimax_pred(df_live, crypto, p, i, q, sarimax_model, days, sp, si, sq, seasonal_factor,
                                     start_p_order, start_i_order, start_q_order, max_p_order, max_i_order, max_q_order,
                                     auto_arima_seasonal_factor, auto_arima_seasonal, auto_arima_stationary,
                                     auto_arima_information_criterion, auto_arima_method)

    return results, pred_fig, sarimax_model
