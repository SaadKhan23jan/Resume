import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# This order means the order in which the page will be shown
dash.register_page(__name__, path='/', order=0)
layout = html.Div([
    dcc.Markdown('# Saad Khan', style={'textAlign': 'center'}),
    dcc.Markdown('Duisburg NRW, Germany', style={'textAlign': 'center'}),
    dcc.Markdown('### Professional Summary', style={'textAlign': 'center'}),
    html.Hr(),
    dcc.Markdown('Young, talented, energetic, open-minded, and hard-working person, always ready to learn new things\n'
                 'and work best in a team. Learning new things especially related to technology always interested me.\n'
                 'As a Mechanical Engineer, always been interested to solve mathematical and analytical problems.\n'
                 'Self-taught Data Analysis and Machine learning along with Python, pandas, matplotlib, seaborn,\n'
                 'sklearn, TensorFlow, statsmodel, etc, visualization software Tableau, Power BI, and CAD software\n'
                 'PTC Creo and Solidworks.', style={'textAlign': 'center', 'white-space': 'pre'}),
    dcc.Markdown('### Skills', style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
            * Python Programmer
            * Data Analysis
            * Pandas, NumPy, Seaborn
            * Matplotlib, DASH, Plotly
            * Tableau/Power BI
            * Dosimis-3
            ''')
        ], width={"size": 3, "offset": 1}),
        dbc.Col([
            dcc.Markdown('''
            * ScikitLearn, Scipy, StatsModel
            * FBProphet, TensorFlow
            * Word, Excel, PowerPoint
            * PTC Creo, SolidWorks
            * Camunda Modeler, Cameo
            * System Modeler, KeyTech PLM''')
        ], width=3)
    ], justify='center'),

    dcc.Markdown('### Work History', style={'textAlign': 'center'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('Feb 2021 – Present', style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Student Job\n'
                         'Wuppertal, Germany', style={'white-space': 'pre'}, className='ms-3'),
            html.Ul([
                html.Li('Online Products and Store Management'),
                html.Li('Product Technical Data, Price Research, Excel, Magento')
            ])
        ], width=5),
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('April 2022 – Dec 2022', style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Master’s Thesis Project\n'
                         'Duisburg, Germany', style={'white-space': 'pre'}, className='ms-3'),
            html.Ul([
                html.Li('MVR measurement of Laser Sintering’s Materials'),
                html.Li('Technical and Mathematical Analysis of the Experimental Data'),
                html.Li('Mathematical evaluation & development of a model for MVR measurements to predict the quality '
                        'of mixed powders in Laser Sintering')
            ])
        ], width=5),

    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('Jun 2018 – Sept 2019', style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Jun 2018 – Sept 2019\n'
                         'Swat, Pakistan', style={'white-space': 'pre'}, className='ms-3'),
            html.Ul([
                html.Li('Lecturer of Physics and Mathematics'),
            ])
        ], width=5),

    ], justify='center'),

    dcc.Markdown('### Education', style={'textAlign': 'center'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('Oct 2020 – Mar 2023', style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Universität Duisburg-Essen\n'
                         'Duisburg, Germany', style={'white-space': 'pre'}, className='ms-3'),
            html.Ul([
                html.Li('Production and Logistics'),
                html.Li('Manufacturing, Additive Manufacturing'),
                html.Li('Supply Chain, Logistics')
            ])
        ], width=5),
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('Sept 2014 – Jun 2018', style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Bachelor Of Mechanical Engineering\n'
                         'Islamabad, pakistan', style={'white-space': 'pre'}, className='ms-3'),
            html.Ul([
                html.Li('Mechanics of Machine'),
                html.Li('Design of Mechanical Parts'),
                html.Li('CAD')
            ])
        ], width=5),
    ], justify='center'),

])
