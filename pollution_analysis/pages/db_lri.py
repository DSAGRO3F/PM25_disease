
import dash
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
#import plotly.graph_objects as go
import os

"""layout design"""
dash.register_page(__name__,
                    path='/lri',
                    title='db-lri',
                    name='db-lri',
                    location="sidebar")



"""layout"""
layout = html.Div([
    html.Div(id='words-output', children=[]),
    dash_table.DataTable(id='table',
                         data=[],
                         page_size=10)
    ])


@callback(
    Output('words-output', 'children'),
    Input('store-words', 'data')
    )
def return_val(data):
    print(f'data_lri: {data}')
    return
    
    
@callback(
    [Output('table', 'data'),
     Output('table', 'columns')],
    Input('store-1', 'data')
    )
def df_table(data):
    df = pd.DataFrame(data)
    rows = df.to_dict('records')
    columns = [{"name": str(col), "id": col} for col in df.columns]
    
    print(f'columns: {columns}')
    return rows, columns









