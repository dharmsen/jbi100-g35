from dash import dcc, html
from jbi100_app.main import app
from dash.dependencies import Input, Output

# Stores visualization control panels that pop up when user hovers over vis icons.

# Generates the control panel that appears when user hovers over vis icons.
def generate_control_panel(visId: int):
    # TODO: add custom behaviour depending on visId
    return html.Span(
        className="tooltiptext",
        children=[
            html.Div(
                className="div-inside-span",
                children=[
                    "components",
                    dcc.RangeSlider(
                        className='my-range-slider',
                        id="range-slider-"+str(visId),
                        min=0,
                        max=20,
                        step=0.5,
                        value=[5, 15]
                    ),
                    html.Div(id="output-"+str(visId))
                ]
            )
        ]
    )

# @app.callback(
#     Output("output-1", "children"),
#     Input("range-slider-1", "value")
# )
# def update_out_div(input_value):
#     return "Output {}".format(input_value)