import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import warnings
warnings.filterwarnings("ignore")

dash.register_page(__name__)

layout = html.Div([
    dcc.Markdown("# These Projects are available on my Github Profile", style={'textAlign': 'center'}),
    dcc.Markdown('## Please click on buttons to open the project', style={'textAlign': 'center'}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Button("Data Visualization and Machine Learning Web App", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/Machine-Learning-Classification-Algorithms"),
        ]),
        dbc.Col([
            dbc.Button("Cryptocurrency Price Prediction with Machine Learning", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/Open-Source-Projects/blob/main/012%20-%20Cryptocurrency%20Price%20Prediction%20with%20Machine%20Learning.ipynb"),
        ]),
        dbc.Col([
            dbc.Button("Data Visualization with Plotly", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/Kaggle-Projects/blob/main/Intermediate%20visualization%20tutorial%20using%20Plotly.ipynb"),
        ]),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Button("Linear Regression Project", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/Final%20Project%20-%20Linear%20Regression%20-%20Machine%20Learning.ipynb"),
        ]),
        dbc.Col([
            dbc.Button("Feature Engineering Project", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/Project%20-%20Feature%20Engineering%20and%20Perdictive%20Machine%20Learning.ipynb"),
        ]),
        dbc.Col([
            dbc.Button("Logistic Regression Project", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/Final%20Project%20-%20Logistic%20Regression.ipynb"),
        ]),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Button("Logistics Regression Project 2", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/Project%202%20-%20Logistic%20Regression.ipynb"),
        ]),
        dbc.Col([
            dbc.Button("KNN - K Nearest Neighbors - Classification Project", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/Project%20-%201%20-%20KNN%20-%20K%20Nearest%20Neighbors%20-%20Classification.ipynb"),
        ]),
        dbc.Col([
            dbc.Button("Principal Component Analysis Project", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/Project%20-%20Principal%20Component%20Analysis.ipynb"),
        ]),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Button(" Supervised Learning Project", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/Project%20-%20Supervised%20Learning.ipynb"),
        ]),
        dbc.Col([
            dbc.Button("Data Analysis Capstone Project", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/00-Capstone-Project.ipynb"),
        ]),
        dbc.Col([
            dbc.Button("KMeans Classification Project", target="_blank",
                       style={'borderRadius': '50%', 'textAlign': 'center', 'display': 'inline-block',
                              'fontSize': '25px', 'border': '5px solid Lightgreen'},
                       href="https://github.com/SaadKhan23jan/My-Data-Data-Analysis-and-Machine-Learning-Projects/blob/main/Project%20-%20KMeans.ipynb"),
        ]),
    ]),
])