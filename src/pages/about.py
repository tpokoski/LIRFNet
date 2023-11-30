import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                    path='/',
                    name='Home')

# About Page information
layout = html.Div([
    dbc.Row([
        html.Img(src='assets/IMG_0208.JPG', className='responsive-image')
        ]),
    dcc.Markdown("""
        ## Maize Yield and Water Use Data

        This dataset was collected over two years, 2012–2013, on maize under 
        12 irrigation treatments with varying levels of deficit during 
        late-vegetative and grain-filling growth stages in semi-arid 
        Northern Colorado supplied with surface drip irrigation. The 
        dataset, which can be found online at the USDA National Agricultural 
        Library data repository (doi: [10.15482/USDA.ADC/1439968](https://data.nal.usda.gov/dataset/usda-ars-colorado-maize-water-productivity-dataset-2012-2013)), includes:

        * Hourly weather data
        * Plant growth and canopy development over the season
        * Final biomass, yield and harvest index
        * Daily water balance data including irrigation, precipitation, 
        soil water content, and estimates of crop evapotranspiration
        * Soil parameters for the site
        * Data from a previous experiment on maize with different 
        treatments (doi: [10.15482/USDA.ADC/1254006](https://data.nal.usda.gov/dataset/usda-ars-colorado-maize-water-productivity-dataset-2008-2011))

        https://www.sciencedirect.com/science/article/pii/S235234091831357X
        
        The purpose of this web application is to visualize this collected
        data on a spatial scale, as well as a line chart for the entire 
        length of the time series. 
    """)
])
