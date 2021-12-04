from dash import dcc, html
from jbi100_app.views.visControlPanel import generate_control_panel
from jbi100_app.main import app
from dash.dependencies import Input, Output

""""
    Stores some components for layout
"""


# Returns a nav bar
def generate_nav_bar():
    return html.Div(
        id="nav-bar",
        children=[
            html.Ul(
                children=[
                    # TODO: link anchors to pages
                    html.Li(
                        children=[
                            html.A(
                                children=["Homepage"], href="#")]),
                    html.Li(
                        children=[
                            html.A(
                                children=["Visualizations"], href="#")]),
                    html.Li(
                        children=[
                            html.A(
                                children=["About"], href="#")]),
                    html.Li(
                        children=[
                            html.A(
                                children=["Help"], href="#")]),
                ]
            )
        ]
    )


def generate_basic_layout():
    return html.Div(
        id="vis",
        children=[
            html.Div(
                id="vis-controls",
                children=[
                    html.H4(children=["Visualization Controls"])
                    # TODO: add some controls here
                ]
            ),
            html.Div(
                id="vis-container",
                children=[
                    html.H4(children=["Visualizations"])
                    # TODO: vis goes here
                ]
            )
        ],
    )

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Each visualization is assigned a unique id that informs drawer what items are needed inside the control panel
def generate_hover_over_control_panel(visId: int):
    return html.Div(
        className="tooltip",
        children=[
            html.Img(
                # src="/assets/bootstrap-icons-1.7.2/clipboard-data.svg",
                src="/assets/bootstrap-icons-1.7.2/file-earmark-bar-graph.svg",
                alt="Bootstrap",
                width="64",
                height="64"
            ),
            "Vis" + str(visId),
            generate_control_panel(visId)
        ]
    )

# Generates the side bar for main page
def generate_side_bar():
    return html.Div(
        id="side-bar",
        children=[
            generate_hover_over_control_panel(1),
            generate_hover_over_control_panel(2),
            generate_hover_over_control_panel(3),
            generate_hover_over_control_panel(4)
        ]
    )

# Generates visualization container for main page
def generate_vis_container():
    return html.Div(
        id="vis-new-container",
        children=[
            html.Div(
                className="visBox",
                id="vis1",
                children=["vis1"]
            ),
            html.Div(
                className="visBox",
                id="vis2",
                children=["vis2"]
            ),
            html.Div(
                className="visBox",
                id="vis3",
                children=["vis3"]
            ),
            html.Div(
                className="visBox",
                id="vis4",
                children=["vis4"]
            ),
        ]
    )


def generate_new_layout():
    return html.Div(
        id="vis",
        children=[
            generate_side_bar(),
            generate_vis_container()
        ]
    )

# Quick test to see if control panel can send data to vis boxes (answer: yes they can)
# Looks like each vis box will need its own callback function
@app.callback(
    Output("vis1", "children"),
    Input("range-slider-1", "value")
)
def update_out_div(input_value):
    return "Vis1: {}".format(input_value)