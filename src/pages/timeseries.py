import dash
from dash import html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd

dash.register_page(__name__,
                    name='Time-Series Data')

# Now bring in a SQLite table as a dataframe
def query_db(query):
    conn = sqlite3.connect('2012corn.sqlite')
    cursor = conn.cursor()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# About Page information
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Select Dataset", className="card-title"),
                    dbc.Select(
                        id='data-dropdown',
                        options=[
                            {'label': 'Weather', 'value': 'Weather data'},
                        ],
                        value='Weather data'
                    )
                ])
            ])
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='time-series-chart')
        ], width=12)
    ])
], fluid=True)

# Callback to update graph
@callback(
    Output('time-series-chart', 'figure'),
    Input('data-dropdown', 'value')
)
def update_graph(selected_data):
    query = f"""
                SELECT * FROM "{selected_data}"
                """
    df = query_db(query)
   # Create figure
    fig = go.Figure()

    # Add trace
    fig.add_trace(go.Scatter(x=df['TIMESTAMP'], y=df['AirTemp_C'], name='Air Temp'))
    fig.add_trace(go.Scatter(x=df['TIMESTAMP'], y=df['RH_fraction'], name='RH Fraction'))
    fig.add_trace(go.Scatter(x=df['TIMESTAMP'], y=df['Vap_Press_kPa'], name='Vapor Pressure'))
    fig.add_trace(go.Scatter(x=df['TIMESTAMP'], y=df['HrlySolRad_kJ_m^2_min^1'], name= 'Solar Radiation'))

    # Set title
    fig.update_layout(title_text="Time series with range slider and selectors")

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    return fig