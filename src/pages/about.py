import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__)

# About Page information
layout= html.Div(
    [
        dcc.Markdown("# ThiS IS THe ABOUT Page")
    ]
)
