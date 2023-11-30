import dash
from dash import Input, Output, dcc, html, State
import dash_bootstrap_components as dbc


app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY], use_pages=True)
# Line needed for deployment
server = app.server


# Setting up the layout
# --------------------------------------------------------------
# Define the toggler and the collapsible sidebar
navbar_toggler = dbc.Button(
    html.Span(className="navbar-toggler-icon"), id="navbar-toggler", color="info", className="mb-3"
)
collapsible_sidebar = dbc.Collapse(
    dbc.Nav(
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
    ),
    id="sidebar-collapse",
    is_open=True,
)

# App layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.Div(
                        html.H1('Limited Irrigation Research Farm', className='text-center'),
                        className='py-1 my-1 bg-primary' 
                    ),
                    navbar_toggler,
                ],
                width=12
            ),
            justify="center",
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(
                    collapsible_sidebar, 
                    xs=4, sm=4, md=2, lg=2, xl=2, xxl=2, 
                    id="sidebar-column"
                ),
                dbc.Col(
                    dash.page_container,
                    xs=8, sm=8, md=10, lg=10, xl=10, xxl=10, 
                    id="page-content-column"
                )  
            ]
        )
    ],
    fluid=True,
)

# Callback to toggle the sidebar and adjust layout
@app.callback(
    [Output("sidebar-collapse", "is_open"),
     Output("sidebar-column", "class"),
     Output("page-content-column", "class")],
    [Input("navbar-toggler", "n_clicks")],
    [State("sidebar-collapse", "is_open")]
)
def toggle_sidebar(n, is_open):
    if n:
        is_open = not is_open

    # Update classes based on whether the sidebar is open
    sidebar_class = "d-none" if not is_open else "col-12 col-md-2"
    content_class = "col-12" if not is_open else "col-12 col-md-10"

    return is_open, sidebar_class, content_class


if __name__ == '__main__':
    app.run(debug=True)