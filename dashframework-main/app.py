from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from jbi100_app.views.layout import generate_nav_bar, generate_basic_layout, generate_new_layout

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

# Create data
df = px.data.iris()

# df_accident = pd.read_csv('dashframework-main/dft-road-casualty-statistics-accident-1979-2020.csv')
#
# fig = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='number_of_casualties', radius=10,
#                         center=dict(lat=0, lon=180), zoom=0,
#                         mapbox_style="stamen-terrain")
#
# Instantiate custom views
scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)
scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df)

app.layout = html.Div(
    id="app-container",
    children=[
       html.Div(
            id="main",
            children=[
                generate_nav_bar(),
                # generate_basic_layout()
                generate_new_layout()
            ]
        ),

        # # Left column
        # html.Div(
        #     id="left-column",
        #     className="three columns",
        #     children=make_menu_layout()
        # ),
        #
        # # Right column
        # html.Div(
        #     id="right-column",
        #     className="nine columns",
        #     children=[
        #         # fig
        #     ],
        # ),
    ],
)

# Define interactions
# @app.callback(
#     Output(scatterplot1.html_id, "figure"), [
#         Input("select-color-scatter-1", "value"),
#         Input(scatterplot2.html_id, 'selectedData')
#     ])
# def update_scatter_1(selected_color, selected_data):
#     return scatterplot1.update(selected_color, selected_data)
#
#
# @app.callback(
#     Output(scatterplot2.html_id, "figure"), [
#         Input("select-color-scatter-2", "value"),
#         Input(scatterplot1.html_id, 'selectedData')
#     ])
# def update_scatter_2(selected_color, selected_data):
#     return scatterplot2.update(selected_color, selected_data)

if __name__ == '__main__':
    app.run_server(debug=False)  # why debug not working :(
