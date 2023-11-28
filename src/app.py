import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Input, Output, dcc, html
import json
import sqlite3
import dash_bootstrap_components as dbc
import datetime

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY], use_pages=True)
# Line needed for deployment
server = app.server


# Setting up the layout
# --------------------------------------------------------------
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page['name'], className='ms-2'),
            ],
            href=page['path'],
            active='exact',            
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H1('Limited Irrigation Research Farm'),
                html.Br(),
            ],
            align='center',
        ),
        
        dbc.Row(
            [
              dbc.Col(
                  [
                      sidebar
                  ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2
              ),
              dbc.Col(
                  [
                      dash.page_container
                  ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10
              )  
            ]
        )

    ],
    fluid=True,
)



if __name__ == '__main__':
    app.run(debug=True)