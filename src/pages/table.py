import dash
from dash import dcc, html, callback, dash_table, Input, Output
import plotly.express as px
import sqlite3
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                    path='/table',
                    name='Data Table')

# Database Access setup
# Now bring in a SQLite table as a dataframe
def query_db(query):
    conn = sqlite3.connect('2012corn.sqlite')
    cursor = conn.cursor()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df



controls = dbc.Card(
    [
        dbc.CardHeader("Data Filters"),
        dbc.CardBody(
            [
                dbc.CardGroup(
                    [
                        dbc.Label("Table Selection"),
                        dbc.Select(id='table_select',
                                   options=[
                                       {'label': 'Annual data by plot', 'value': 'Annual data by plot'},
                                       {'label': 'Plant Ht by Plot', 'value': 'Plant Ht by Plot'},
                                       {'label': 'Canopy Cover by Plot', 'value': 'Canopy Cover by Plot'},
                                       {'label': 'Soil Field Capacity', 'value': 'Soil Field Capacity'},
                                       {'label': 'Weather Data', 'value': 'Weather Data'},
                                       {'label': 'LAI by Plot', 'value': 'LAI by Plot'},
                                       {'label': 'Water Balance ET', 'value': 'Water Balance ET'},
                                       ],
                                   value='Annual data by plot'
                                   ),
                    ]
                ),
            ]
        ),
    ],
)

layout = html.Div(
    [
        dbc.Row(
                [
                    dcc.Markdown('Data Table'),
                ]    
        ),
        dbc.Row(
            [
                dbc.Col(controls)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dash_table.DataTable(
                    id='datatable',
                    style_header={
                        'backgroundColor': 'rgb(30, 30, 30)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },
                    style_table={'overflowX': 'auto',
                                 'overflowY': 'auto',
                                 'height':'300px'
                                }
                    ), 
                )
            ]
        ),
    ]
)

@callback(
    Output(component_id='datatable', component_property='data'),
    Input(component_id='table_select', component_property='value')
)
def update_table(table):
    query = f"""
        SELECT * FROM "{table}"   
        """
    df = query_db(query)
    return df.to_dict('records')
    