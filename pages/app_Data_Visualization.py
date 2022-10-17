import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
from plots import eda_graph_plot


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    # define data frame as global
    global df
    global dict_col
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        elif 'xls' in filename:
            # Assume that the user uploaded an Excel file
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    df = df.dropna()
    dict_col = []
    for col in df.columns:
        dict_col.append({'label': col, 'value': col})


dash.register_page(__name__)
layout = html.Div([

    # This div container is for uploading file (uploaded when clicked the "Upload File" button)
    # This is connected to "app.callback() 1"
    html.Div([
        dcc.Upload(id='upload-data_da',
                   children=html.Div(['Drag and Drop or ', html.A('Select a Single File')]),
                   style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '2px',
                          'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center',
                          'backgroundColor': 'Lightgreen', 'color': 'black', 'fontWeight': 'bold'},
                   # Do not allow multiple files to upload
                   multiple=False
                   ),
        # The below line is for if we want to show the uploaded file as Data Table, the button is inside div to style it
        # html.Div(id='output-data-upload_1', hidden=True),
        html.Div(dbc.Button('Click to Upload File', id='upload_button_da',
                            style={'border': '2px solid Lightgreen', 'borderRadius': '20px'}),
                 style={'alignItem': 'center', 'display': 'flex', 'justifyContent': 'center', 'margin': '20px'},),
        html.Div(html.Output(id='file_uploaded_da'),
                 style={'alignItem': 'center', 'display': 'flex', 'justifyContent': 'center', 'color': 'black'},),

    ], style={'background': 'white'}),
    html.Br(),

    # This Div is for Explanatory Data Analysis (EDA)
    # This is connected to "app.callback() 2" and "app.callback() 3"
    html.Div([
        html.Label('Explanatory Data Analysis', style={'fontSize': '50px', 'fontWeight': 'bold'}),
        html.Br(),

        dbc.Row([
            dbc.Col([
                html.Label('Select X Feature', style={'width': '100%'}),
                dcc.Dropdown(id="x_axis_features_da", style={'width': '100%'}),
                html.Label('Select y Feature', style={'width': '100%'}),
                dcc.Dropdown(id="y_axis_features_da", style={'width': '100%'}),
                html.Label('Select Graph Type', style={'width': '100%'}),
                dcc.Dropdown(id="graph_type_da", options=[{'label': 'Scatter', 'value': 'Scatter'},
                                                          {'label': 'Line', 'value': 'Line'},
                                                          {'label': 'Area', 'value': 'Area'},
                                                          {'label': 'Bar', 'value': 'Bar'},
                                                          {'label': 'Funnel', 'value': 'Funnel'},
                                                          {'label': 'Timeline', 'value': 'Timeline'},
                                                          {'label': 'Pie', 'value': 'Pie'},
                                                          {'label': 'Subburst', 'value': 'Subburst'},
                                                          {'label': 'Treemap', 'value': 'Treemap'},
                                                          {'label': 'Icicle', 'value': 'Icicle'},
                                                          {'label': 'Funnel Area', 'value': 'Funnel Area'},
                                                          {'label': 'Histogram', 'value': 'Histogram'},
                                                          {'label': 'Box', 'value': 'Box'},
                                                          {'label': 'Violin', 'value': 'Violin'},
                                                          {'label': 'Strip', 'value': 'Strip'},
                                                          {'label': 'ECDF', 'value': 'ECDF'},
                                                          {'label': 'Density Heatmap', 'value': 'Density Heatmap'},
                                                          {'label': 'Density Contour', 'value': 'Density Contour'},
                                                          {'label': 'Imshow', 'value': 'Imshow'},
                                                          {'label': 'Scatter Geo', 'value': 'Scatter Geo'}],
                             value='Histogram', style={'width': '100%'}),
                html.Label('Orientation', style={'width': '100%'}),
                dcc.Dropdown(id="orientation_da", options=[{'label': 'Vertical', 'value': 'v'},
                                                           {'label': 'Horizontal', 'value': 'h'}, ],
                             style={'width': '100%'}),
            ]),

            dbc.Col([
                html.Label('Color', style={'width': '100%'}),
                dcc.Dropdown(id="color_da", style={'width': '100%'}),
                html.Label('Symbol', style={'width': '100%'}),
                dcc.Dropdown(id="symbol_da", style={'width': '100%'}),
                html.Label('Size', style={'width': '100%'}),
                dcc.Dropdown(id="size_da", style={'width': '100%'}),
                html.Label('Hover Name', style={'width': '100%'}),
                dcc.Dropdown(id="hover_name_da", style={'width': '100%'}, ),
            ]),

            dbc.Col([
                html.Label('Hover Data', style={'width': '100%'}),
                dcc.Dropdown(id="hover_data_da", style={'width': '100%'}, multi=True),
                html.Label('Custom Data', style={'width': '100%'}),
                dcc.Dropdown(id="custom_data_da", style={'width': '100%'}, multi=True),
                html.Label('Text', style={'width': '100%'}),
                dcc.Dropdown(id="text_da", style={'width': '100%'}),
                html.Label('Facet Row', style={'width': '100%'}),
                dcc.Dropdown(id="facet_row_da", style={'width': '100%'}),
            ]),

            dbc.Col([
                html.Label('Facet Column', style={'width': '100%'}),
                dcc.Dropdown(id="facet_col_da", style={'width': '100%'}),
                html.Label('Width of Figure', style={'width': '100%'}),
                dcc.Input(id='width_da', style={'width': '100%'}, type='number', inputMode='numeric', step=1, min=0),
                html.Label('Height of Figure', style={'width': '100%'}),
                dcc.Input(id='height_da', style={'width': '100%'}, type='number', inputMode='numeric', step=1, min=0),
                html.Label('Sort the Data by', style={'width': '100%'}),
                dcc.Dropdown(id='sort_by_da', style={'width': '100%'}),
            ]),

            dbc.Col([
                html.Label('Latitude', style={'width': '100%'}),
                dcc.Dropdown(id="latitude_da", style={'width': '100%'}),
                html.Label('Longitude', style={'width': '100%'}),
                dcc.Dropdown(id='longitude_da', style={'width': '100%'}),
                html.Label('Locations', style={'width': '100%'}),
                dcc.Dropdown(id='locations_da', style={'width': '100%'}),
                html.Label('Location Mode', style={'width': '100%'}),
                dcc.Dropdown(id='locationmode_da', style={'width': '100%'},
                             options=[{'label': 'ISO-3', 'value': 'ISO-3'},
                                      {'label': 'USA-states', 'value': 'USA-states'}, ], ),
            ])
        ]),
        html.Br(),
        html.Div(dbc.Button("Plot Graph", id="plot_graph_da", size="lg", className="me-1",
                            style={'border': '2px solid Lightgreen', 'borderRadius': '20px'}),
                 style={'alignItem': 'center', 'justifyContent': 'center',  'display': 'flex', 'marginBottom': '20px'}),

        dcc.Graph(id="eda_graph_da"),
    ], style={'backgroundColor': 'Lightblue', 'color': 'black'}),
    html.Br(),

    # This div container is for options of hiding Data Frame, showing only head with 5 row on full Data Frame
    # This is connected to app.callback() 9
    html.Div([
        html.Label('Show the DataFrame', style={'color': 'black', 'fontSize': '20px', 'paddingRight': '20px'}),
        dcc.RadioItems(id='show_df_da', options=[{'label': 'Full   ', 'value': 'Full'},
                                                 {'label': 'Head', 'value': 'Head'},
                                                 {'label': 'No', 'value': 'No'}, ],
                       value='No', style={'fontSize': '20px', 'color': 'black'}, inputStyle={'margin': '10px'}),
    ], style={'backgroundColor': '#f3f2f5', 'justifyContent': 'center', 'alignItems': 'center', 'display': 'flex',
              'border': '2px solid black', 'borderRadius': '10px'}),
    html.Br(),

    # This div container is for the results of above options to print the Data Frame as per the chosen option
    # This is connected to "app.callback() 5" and # app.callback() 9 # can be one, will edit later
    html.Div(id='df_div_da',
             children=[
                 dash_table.DataTable(id='dataframe_da', style_table={'overflowX': 'auto'},
                                      style_cell={'height': 'auto', 'minWidth': '100px', 'width': '100px',
                                                  'maxWidth': '180px', 'whiteSpace': 'normal'},
                                      style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},
                                      style_data={'color': 'black', 'backgroundColor': 'white',
                                                  'border': '2px solid blue'},
                                      filter_action='native'
                                      ),
             ], hidden=True),
    html.Br(),

], style={'background': 'Lightgreen'})


# This is for Uploading the csv file. it will only upload if the button is clicked
# At the same time it will call the "parse_contents" function to make global Data Frame df
# This will also create labels for EDA Analysis
# app.callback() 1
@callback(
    # Output('output-data-upload', 'children'),
    Output('file_uploaded_da', 'children'),
    Output('x_axis_features_da', 'options'),
    Output('y_axis_features_da', 'options'),
    Output('color_da', 'options'),
    Output('symbol_da', 'options'),
    Output('size_da', 'options'),
    Output('hover_name_da', 'options'),
    Output('hover_data_da', 'options'),
    Output('custom_data_da', 'options'),
    Output('text_da', 'options'),
    Output('facet_row_da', 'options'),
    Output('facet_col_da', 'options'),
    Output('sort_by_da', 'options'),
    Output('latitude_da', 'options'),
    Output('longitude_da', 'options'),
    Output('locations_da', 'options'),
    Input('upload_button_da', 'n_clicks'),
    State('upload-data_da', 'contents'),
    State('upload-data_da', 'filename'),
    State('upload-data_da', 'last_modified'),
    prevent_initial_call=True)
def upload_dataframe(n_clicks, content, filename, date):
    # print(type(df))#this will show data type as a pandas dataframe
    # print(df)

    if filename is not None:
        children = parse_contents(content, filename, date)

        # initiate list
        options_for_dropdown = []
        for idx, colum_name in enumerate(df.columns):
            options_for_dropdown.append(
                {
                    'label': colum_name,
                    'value': colum_name
                }
            )
        return [f'{filename} is Uploaded Successfully...', options_for_dropdown, options_for_dropdown,
                options_for_dropdown, options_for_dropdown, options_for_dropdown, options_for_dropdown,
                options_for_dropdown, options_for_dropdown, options_for_dropdown, options_for_dropdown,
                options_for_dropdown, options_for_dropdown, options_for_dropdown, options_for_dropdown,
                options_for_dropdown]
    else:
        children = parse_contents(content, filename, date)
        return [f'No File is Uploaded...', None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None]


# This app.callback() is for generating Graph
# app.callback() 3
@callback(Output('eda_graph_da', 'figure'),
          [Input('plot_graph_da', 'n_clicks'),
           State('x_axis_features_da', 'value'),
           State('y_axis_features_da', 'value'),
           State('graph_type_da', 'value'),
           State('color_da', 'value'),
           State('symbol_da', 'value'),
           State('size_da', 'value'),
           State('hover_name_da', 'value'),
           State('hover_data_da', 'value'),
           State('custom_data_da', 'value'),
           State('text_da', 'value'),
           State('facet_row_da', 'value'),
           State('facet_col_da', 'value'),
           State('orientation_da', 'value'),
           State('width_da', 'value'),
           State('height_da', 'value'),
           State('sort_by_da', 'value'),
           State('latitude_da', 'value'),
           State('longitude_da', 'value'),
           State('locations_da', 'value'),
           State('locationmode_da', 'value'), ],
          prevent_initial_call=True)
def update_graph(n_clicks, x_axis_features, y_axis_features, graph_type, color, symbol, size, hover_name, hover_data,
                 custom_data, text, facet_row, facet_col, orientation, width, height, sort_by, latitude_da,
                 longitude_da, locations_da, locationmode_da):
    return eda_graph_plot(df, x_axis_features, y_axis_features, graph_type, color, symbol, size, hover_name, hover_data,
                          custom_data, text, facet_row, facet_col, orientation, width, height, sort_by,
                          latitude_da, longitude_da, locations_da, locationmode_da)


# This app.callback() is for showing the  Data Frame as per the choice
# app.callback() 9
@callback([Output('df_div_da', 'hidden'),
           Output('dataframe_da', 'data'),
           Output('dataframe_da', 'columns'), ],
          [Input('show_df_da', 'value'), ],
          prevent_initial_call=True)
def show_dataframe(show_df):
    df_columns = [{'name': col, 'id': col} for col in df.columns]
    df_table = df.to_dict(orient='records')
    if show_df == 'Head':
        df_table = df_table[:5]
        return False, df_table, df_columns
    elif show_df == "Full":
        return False, df_table, df_columns
    else:
        return True, df_table, df_columns
