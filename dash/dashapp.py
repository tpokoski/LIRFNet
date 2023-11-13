import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import json
import sqlite3

app = Dash(__name__)

# Bring in the data
# -------------------------------------------------------------
# First the geojson
with open('LIRF.json') as filepath:
    geojson = json.load(filepath)

# Now bring in a SQLite table as a dataframe
conn = sqlite3.connect('2012corn.sqlite')
cursor = conn.cursor()
query = f"""
SELECT *
FROM 'Canopy Cover by Plot'
"""
df = pd.read_sql_query(query, conn)
conn.close()

dates_test = df['Date'].drop_duplicates()
dates_test = dates_test.tolist()

# Making the map
fig = px.choropleth_mapbox(df, 
                    geojson=geojson,
                    locations='Plot',
                    featureidkey='properties.TrtmPlotID',
                    color='Canopy_Cover',
                    mapbox_style="carto-positron",
                    center = {"lat": 40.4486, "lon": -104.6368},
                    zoom=16.5
                    )
fig.update_layout(
    mapbox_style="white-bg",
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


# --------------------------------------------------------------
app.layout = html.Div(children=[
    html.H1(children='LIRF 2012 Corn Data'),
    html.Div(children="""
             Displaying the 2012 Corn Canopy Cover
             """),
    dcc.Dropdown(id='data_select',
                 options=[
                     {"label": "LAI", "value": "LAI by Plot"},
                     {"label": "Plant Height", "value": "Plant Ht by Plot"},
                     {"label": "Canopy Cover", "value": "Canopy Cover by Plot"}                     
                 ],
                 style={'width':'40%'}
                 ),
    dcc.Slider(
                id='date_slider',
                min=0,
                max=len(df['Date'].unique()),
                step=None,
                value=0,
                marks={i:dates_test[i] for i in range(len(dates_test))}
               ),
    html.Br(),
    dcc.Graph(id='map',
              figure = fig,
              style={"width":"50%"})
    ])

#---------------------------------------------------
# Callback functions
@app.callback(Output(component_id='map', component_property='figure'),
    [Input(component_id='data_select', component_property='value'),
     Input(component_id='date_slider', component_property='value')]
    )
def update_figure(selected_data, selected_date):
    print(dates_test[selected_date])
    filterdf = df[df['Date'] == dates_test[selected_date]]
    print(filterdf)
    fig = px.choropleth_mapbox(filterdf, 
                    geojson=geojson,
                    locations='Plot',
                    featureidkey='properties.TrtmPlotID',
                    color='Canopy_Cover',
                    mapbox_style="carto-positron",
                    center = {"lat": 40.4486, "lon": -104.6368},
                    zoom=16.5
                    )
    fig.update_layout(
        mapbox_style="white-bg",
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
    return fig

if __name__ == '__main__':
    app.run(debug=True)