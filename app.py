#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:39:37 2024

@author: olivierdebeyssac
"""

import dash
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
from dash import dcc
from dash.dependencies import Input, Output
from dash import dash_table
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, 
                use_pages=True,
                external_stylesheets=[dbc.themes.UNITED])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


sidebar = html.Div([
    html.H2("Sidebar", className="display-4"),
    html.Hr(),
    dbc.Nav(
        [dbc.NavLink(
            [html.Div(page['name'], className='ms-2')],
            href=page['path'],
            active='exact') for page in dash.page_registry.values()
            ],
        vertical=True,
        pills=True,
        className='bg-light'
        )
    ],
    style=SIDEBAR_STYLE,
    )




app.layout = dbc.Container([
    html.Div([
        dcc.Store(id='store-1', data={}, storage_type='memory'),
        dcc.Store(id='store-2', data={}, storage_type='memory'),
        dcc.Store(id='store-3', data={}, storage_type='memory'),
        dcc.Store(id='store-4', data={}, storage_type='memory'),
        dcc.Store(id='store-5', data={}, storage_type='memory'),
        dcc.Store(id='store-6', data={}, storage_type='memory'),
        dcc.Store(id='store-7', data={}, storage_type='memory'),
        dcc.Store(id='store-8', data={}, storage_type='memory'),
        dcc.Store(id='store-9', data={}, storage_type='memory'),
        dcc.Store(id='store-10', data={}, storage_type='memory'),
        dcc.Store(id='store-11', data={}, storage_type='memory'),
        dcc.Store(id='store-12', data={}, storage_type='memory'),
        dcc.Store(id='store-13', data={}, storage_type='memory'),
        dcc.Store(id='store-14', data={}, storage_type='memory'),
        dcc.Store(id='store-15', data={}, storage_type='memory'),
        dcc.Store(id='store-16', data={}, storage_type='memory'),
        dcc.Store(id='store-list_dict', data={}, storage_type='memory'),
        dcc.Store(id='store-words', data={}, storage_type='memory'),
        dcc.Store(id='store-years', data={}, storage_type='memory')
        ]),

        
    dbc.Row([
        dbc.Col([
            sidebar],
            xs=4,
            sm=4,
            md=2,
            lg=2,
            xxl=2),
        
        dbc.Col([
            dash.page_container],
            xs=8,
            sm=8,
            md=10,
            lg=10,
            xxl=10),
        ])
    ], 
    fluid=True
    )
        

if __name__ == '__main__':
    app.run(debug=True)




