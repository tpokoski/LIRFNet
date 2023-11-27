import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Input, Output, dcc, html
import json
import sqlite3
import dash_bootstrap_components as dbc
import datetime

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

# Bring in the data
# -------------------------------------------------------------
# First the geojson
with open('LIRF.json') as filepath:
    geojson = json.load(filepath)

# Now bring in a SQLite table as a dataframe
def query_db(query):
    conn = sqlite3.connect('2012corn.sqlite')
    cursor = conn.cursor()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def column_select(selected_data):
    if selected_data == "Canopy Cover by Plot":
        column = 'Canopy_Cover'
    elif selected_data == 'LAI by Plot':
        column = 'LAI'
    elif selected_data == 'Plant Ht by Plot':
        column='Plant_Ht'
    
    return column

# Setting up the layout
# --------------------------------------------------------------
controls = dbc.Card(
    [
        dbc.CardHeader("Data Filters"),
        dbc.CardBody(
            [
                dbc.CardGroup(
                    [
                        dbc.RadioItems(
                            id="year_select",
                            options=[
                                {"label": "2012", "value": 2012},
                                {"label": '2013', "value": 2013}
                            ],
                            value=2012,
                            inline=True
                        ),
                    ]
                ),
                dbc.CardGroup(
                    [
                        dbc.Label("Data Selection"),
                        dbc.Select(
                            id='data_select',
                            options=[
                                {"label": "LAI", "value": "LAI by Plot"},
                                {"label": "Plant Height", "value": "Plant Ht by Plot"},
                                {"label": "Canopy Cover", "value": "Canopy Cover by Plot"}                     
                            ],
                            value="LAI by Plot"
                        ),
                    ]
                ),
            ]
        ),
    ],
)

slider_control = dbc.Card(
            html.Div(
            [
                dbc.Label("Date Select"),
                dcc.Slider(
                    id='date_slider',
                    min=0,
                    max=10,
                    
                    value=0,
                ),
            ]
        ),
)
app.layout = dbc.Container(
    [
        html.H1('LIRF 2012 Corn Data'),
        html.Div("Displaying the 2012 Corn Canopy Cover"),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(controls, md=6, xl=4),  # Adjust the size as needed for the controls
                dbc.Col(slider_control, md=6, xl=8),  # Adjust the size as needed for the slider
            ],
            align='center',
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='map'), md=12),  # Map figure takes full width
            ],
            align='center',
            className="mb-3",  # Add a margin bottom for spacing
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='chart'), md=12),  # Chart figure takes full width
            ],
            align='center',
        ),
    ],
    fluid=True,
)



#---------------------------------------------------
# Callback functions
@app.callback(
    [
        Output(component_id='date_slider', component_property='max'),
        Output(component_id='date_slider', component_property='marks'),
        Output(component_id='date_slider', component_property='step'),
    ],
    [
        Input(component_id='year_select', component_property='value'),
        Input(component_id='data_select', component_property='value'),
        
    ]
)
def update_range(selected_year, selected_data):
    query = f"""
            SELECT * FROM "{selected_data}"
            WHERE Year = {selected_year}    
            """
    df = query_db(query)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%m/%d')
    dates_test = df['Date'].drop_duplicates()
    dates_test = dates_test.tolist()
    max = len(df['Date'].unique())
    marks={i:dates_test[i] for i in range(len(dates_test))}
    step=None
    return max, marks, step

@app.callback(
    Output(component_id='map', component_property='figure'),
    [
        Input(component_id='data_select', component_property='value'),
        Input(component_id='date_slider', component_property='value'),
        Input(component_id='year_select', component_property='value'),
        Input(component_id='chart', component_property='clickData')
    ]
)
def update_figure(selected_data,selected_date,selected_year, clickData):
    query = f"""
            SELECT * FROM "{selected_data}"
            WHERE Year = {selected_year}    
            """
    df = query_db(query)
    col = column_select(selected_data)
    dates_test = df['Date'].drop_duplicates()
    dates_test = dates_test.tolist()
    filterdf = df[df['Date'] == dates_test[selected_date]]
    

    
    fig = px.choropleth_mapbox(filterdf, 
                    geojson=geojson,
                    locations='Plot',
                    featureidkey='properties.TrtmPlotID',
                    color=col,
                    range_color=[df[col].min(), df[col].max()],
                    color_continuous_scale="rdylgn",
                    mapbox_style="carto-positron",
                    center = {"lat": 40.4486, "lon": -104.6368},
                    zoom=16.3
                    )
    fig.update_layout(
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    if clickData is not None:
        curveNumber = clickData["points"][0]['curveNumber']
        print(curveNumber)
        traces = fig['data']
        fig['data'][curveNumber]['marker']['color'] = "#FFFFFF"
        return fig
    else:
        return fig

@app.callback(
    Output(component_id='chart', component_property='figure'),
    [
        Input(component_id='data_select', component_property='value'),
        Input(component_id='year_select', component_property='value'),
    ]
)
def update_chart(selected_data, selected_year):
    query = f"""
            SELECT * FROM "{selected_data}"
            WHERE Year = {selected_year}    
            """
    df = query_db(query)
    col = column_select(selected_data)
    fig = px.line(df, x='Date', y=col, color='Plot')
    return fig


if __name__ == '__main__':
    app.run(debug=True)