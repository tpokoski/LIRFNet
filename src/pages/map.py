import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Input, Output, dcc, html, callback
import json
import sqlite3
import dash_bootstrap_components as dbc
import datetime

dash.register_page(__name__)
# Line needed for deployment
# Bring in the data
# -------------------------------------------------------------
# First the geojson
with open('sorted_LIRF.json') as filepath:
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
    elif selected_data == 'SWC_15':
        column='SWC_15'
    elif selected_data == 'SWC_30':
        column='SWC_30'
    elif selected_data == 'SWC_60':
        column='SWC_60'
    elif selected_data == 'SWC_90':
        column='SWC_90'
    elif selected_data == 'SWC_120':
        column='SWC_120'
    elif selected_data == 'SWC_150':
        column='SWC_150'
    elif selected_data == 'SWC_200':
        column='SWC_200'
    elif selected_data == 'SWD_RZ':
        column='SWD_RZ'
               
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
                        )
                    ]
                ),
                dbc.CardGroup(
                    [
                        dbc.RadioItems(
                            id='treatment_select',
                            options=[
                                {'label': 'Plot', 'value': 0},
                                {'label': 'Treatment', 'value': 1}                                
                            ],
                            value=0,
                            inline=True
                        ),
                    ]
                ),
                dbc.CardGroup(
                    [
                        dbc.Label("Data Selection"),
                        dbc.Select(id='data_select'),
                    ]
                ),
            ]
        ),
    ],
)

slider_control = dbc.Card(
            [
                dbc.CardHeader("Date Select"),
                dbc.CardBody(
                    dcc.Slider(
                        id='date_slider',
                        min=0,
                        max=10,                        
                        value=0,
                ),
                )

            ]
)
layout = dbc.Container(
    [        
        dbc.Row(
            [
                dbc.Col(slider_control, md=12),  # Slider control takes full width at the top
            ],
            align='center',
        ),

        dbc.Row(
                html.Div(  # Flex container
                [
                    dbc.Col(html.Div(controls, style={"display": "flex", "flexDirection": "column", "flexGrow": 1}), md=4, xl=4),  # Flex item for controls
                    dbc.Col(dcc.Graph(id='map', style={"display": "flex", "flexDirection": "column", "flexGrow": 1}), md=8, xl=8),  # Flex item for map
                ],
                style={"display": "flex", "flexDirection": "row", 'height': '100%'}
            ),
            align='center',
            className="mb-3",  # Add a margin bottom for spacing
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='chart'), md=12),  # Chart takes full width at the bottom
            ],
            align='center',
        ),
    ],
    fluid=True,
)



#---------------------------------------------------
# Callback functions
@callback(
    [
        Output(component_id='date_slider', component_property='max'),
        Output(component_id='date_slider', component_property='marks'),
        Output(component_id='date_slider', component_property='step'),
    ],
    [
        Input(component_id='year_select', component_property='value'),
        Input(component_id='data_select', component_property='value'),
        Input(component_id='treatment_select', component_property='value'),
        
    ]
)
def update_range(selected_year, selected_data, trt):
    if trt == 0:
        query = f"""
                SELECT * FROM "{selected_data}"
                WHERE Year = {selected_year}    
                """
    else: 
        query = f"""
                SELECT * FROM "Water Balance ET"
                WHERE (Year = {selected_year} AND "{selected_data}" IS NOT NULL)    
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


@callback(
    [
        Output(component_id='data_select', component_property='options'),
        Output(component_id='data_select', component_property='value'),
    ],
    Input(component_id='treatment_select', component_property='value')
)
def update_dropdown(selected_treatment):
    if selected_treatment ==0:
        options=[
            {"label": "LAI", "value": "LAI by Plot"},
            {"label": "Plant Height", "value": "Plant Ht by Plot"},
            {"label": "Canopy Cover", "value": "Canopy Cover by Plot"}                     
        ]
        value="LAI by Plot"
    elif selected_treatment == 1:   
        options=[
            {"label": "SWC_15", "value": "SWC_15"},
            {"label": "SWC_30", "value": "SWC_30"}, 
            {"label": "SWC_60", "value": "SWC_60"}, 
            {"label": "SWC_90", "value": "SWC_90"}, 
            {"label": "SWC_120", "value": "SWC_120"}, 
            {"label": "SWC_150", "value": "SWC_150"}, 
            {"label": "SWC_200", "value": "SWC_200"},                     
            {"label": "SWD_RZ", "value": "SWD_RZ"}, 
        ]
        value="SWC_15"
    return options, value

@callback(
    [
        Output(component_id='chart', component_property='figure'),
        Output(component_id='map', component_property='figure')
    ],
    [
        Input(component_id='data_select', component_property='value'),
        Input(component_id='year_select', component_property='value'),
        Input(component_id='treatment_select', component_property='value'),
        Input(component_id='chart', component_property='clickData'),
        Input(component_id='map', component_property='clickData'),
        Input(component_id='date_slider', component_property='value')
    ]
)
def update_visualizations(selected_data, selected_year, trt, click_chart, click_map, selected_date):
    

    # Create or update the choropleth map
    if trt == 0:
        query = f"""
                SELECT * FROM "{selected_data}"
                WHERE Year = {selected_year}    
                """
        df = query_db(query)
        col = column_select(selected_data)
        dates_test = df['Date'].drop_duplicates()
        dates_test = dates_test.tolist()
        filterdf = df[df['Date'] == dates_test[selected_date]]
        locat='Plot'
    else:
        query = f"""
                SELECT * FROM "Water Balance ET"
                WHERE (Year = {selected_year} AND "{selected_data}" IS NOT NULL)    
                """
        df = query_db(query)
        col = column_select(selected_data)
        dates_test = df['Date'].drop_duplicates()
        dates_test = dates_test.tolist()
        filterdf = df[df['Date'] == dates_test[selected_date]]
        locat="Plot"
    
    fig_map = px.choropleth_mapbox(filterdf, 
                    geojson=geojson,
                    locations= locat,
                    featureidkey='properties.TrtmPlotID',
                    color=col,
                    range_color=[df[col].min(), df[col].max()],
                    color_continuous_scale="rdylgn",
                    mapbox_style="carto-positron",
                    center = {"lat": 40.4486, "lon": -104.6368},
                    zoom=16.8
                    )
    # Update layout to reduce padding and margin
    fig_map.update_layout(
        margin={"r":0, "t":0, "l":0, "b":0}
    )
    fig_map.update_layout(
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
    # Create a mapping from TrtmPlotID to geojson feature index
# Get a list of TrtmPlotID that are present on the map
    trtmplotids_on_map = df['Plot'].unique().tolist()

    # Filter the geojson to include only those features present on the map
    filtered_geojson_features = [feature for feature in geojson['features'] 
                                if feature['properties']['TrtmPlotID'] in trtmplotids_on_map]

    # Now create the mapping dictionary
    plot_id_to_index = {feature['properties']['TrtmPlotID']: i 
                        for i, feature in enumerate(filtered_geojson_features)}
    plot_lookup = {feature['properties']['TrtmPlotID']: feature for feature in geojson['features']}
    plot_names = [feature['properties']['TrtmPlotID'] for feature in geojson['features']]
    sorted_plot = {k: v for v, k in enumerate(sorted(plot_id_to_index.keys()))}
    # Create or update the line chart
    if trt == 0:
        query = f"""
                SELECT * FROM "{selected_data}"
                WHERE Year = {selected_year}    
                """
        df = query_db(query)
        col = column_select(selected_data)
        fig_chart = px.line(df, x='Date', y=col, color='Plot', category_orders=plot_id_to_index)
    else:
        query = f"""
        SELECT * FROM "Water Balance ET"
        WHERE (Year = {selected_year} AND "{selected_data}" IS NOT NULL)    
        """
        df = query_db(query)
        col = column_select(selected_data)
        fig_chart = px.line(df, x='Date', y=col, color='Trt_code')
    
    # Initialize a list for line colors, default to grey (or another default color)
    line_colors = ['grey'] * len(fig_map.data[0].geojson['features'])  # Grey color

    # Update choropleth map based on click data
    if click_chart and 'points' in click_chart and len(click_chart['points']) > 0:
        
        clicked_trace_index = click_chart['points'][0]['curveNumber']
        clicked_plot = fig_chart.data[clicked_trace_index].name

        # Reset all to default color first
        for i in range(len(line_colors)):
            line_colors[i] = 'grey'  # Default color

        # Find the index of the geojson feature for the clicked plot
        if clicked_plot in plot_id_to_index:
            plot_index = plot_id_to_index[clicked_plot]
            sorted_index = sorted_plot[clicked_plot]
            print(plot_index, sorted_index)
            line_colors[sorted_index] = 'white'  # Highlighted line color
    else:
        # Reset map styling if no plot is clicked
        line_colors = ['grey'] * len(line_colors)
    
    # Click-Map isolates the line on the graph
    if click_map is None:
        name='None'
    else:
        name = click_map['points'][0]['location']
        fig_chart.update_traces(visible='legendonly')
        fig_chart.update_traces(visible=True,
                                selector=dict(name=name))

    
    # Update the choropleth map styling
    fig_map.update_traces(marker_line_color=line_colors)
    return fig_chart, fig_map