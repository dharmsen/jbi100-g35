from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import Data
from jbi100_app.visualizations.barchart import Barchart
from jbi100_app.visualizations.map import make_map

from jbi100_app.views.layout import generate_nav_bar, generate_basic_layout, generate_new_layout

from dash import html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from datetime import date

import dash_leaflet as dl

# Get data by making a data object and getting the required dfs from it.
# TODO: uncomment data object once in production, currently comment for quicker start up
# data = Data()
# df_date, df_conditions, df_location, df_severity = data.get_dataframes()

data = Data()
df_date, df_severity, df_location = data.get_dataframes()

# FIXME: accident_index col is killing the table
# df_date.drop('accident_index', inplace=True, axis=1)

# Get filter settings
range_filter_global_settings = data.get_range_filter_global_settings()
date_filter_global_settings = data.get_date_filter_global_settings()

df_date_short = df_date.head(100)
# TODO: do something better with the temp table
table = html.Div(
            id='table-wrapper',
            children=
            dash_table.DataTable(
                id='table',
                style_table={'maxHeight': '250px', 'overflowY' : 'scroll'},
                #maxHeight otherwise table doesnt respect parent div
            )
        )


map = html.Div(
        children=[
            dcc.Graph(id='map', style={'height': '100%'})
        ]
)

# test = make_map(df_location)


from geojson import load
from jbi100_app.visualizations.map_helper import Map_Helper



# df_new = df_location.join(df_date, rsuffix='_b')
df_new = df_location.join(df_severity, rsuffix='_b')

# masker = (df_new['accident_year'] == 2020) | (df_new['accident_year'] == 2019)

print(df_new.columns)

m = make_map(df_new)

# map_maker = Map_Helper(df_new[masker])
# map_maker = Map_Helper(df_location)

with open('jbi100_app/assets/data/mapData.geojson') as f:
        collection = load(f)

# mapy = dl.Map([
#     dl.TileLayer(),
#     dl.GeoJSON(data=collection, cluster=True, superClusterOptions={'minPoints': 10, 'minZoom': 0}),
# ], center=(51.5, -0.1), zoom=1, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})
mapy = None
# cluster size needs some adjustments, zooming in immediately kills performance


# Make simple barchart vis example
# Join together for barchart
df_merged = df_date.join(df_severity, lsuffix='_date', rsuffix='_severity')
grouped = df_merged.groupby('accident_year').agg({'number_of_casualties': 'mean'})
grouped = grouped.reset_index()

simple_barchart = Barchart('accident_year', 'number_of_casualties', grouped)

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="main",
            children=[
                generate_nav_bar(),
                generate_new_layout(range_filter_global_settings, date_filter_global_settings, simple_barchart, mapy)
            ]
        ),
    ],
)


# Global filter callback function
@app.callback(
    Output('table', 'columns'), # TODO: only changing current table, will need to change to other vis' i think
    Output('table', 'data'),
    Input('year-filter-global', 'value'),
    Input('time-filter-global', 'value'),
    Input('vehicles-slider-global', 'value'),
    Input('date-picker-global', 'start_date'),
    Input('date-picker-global', 'end_date'),
)
def global_filter(year_range, time_range, vehicle_no, start_date, end_date):
    print(year_range, time_range, vehicle_no, start_date, end_date)

    # this table takes 2 business days to get rendered
    mask = (df_date['accident_year'] >= year_range[0]) & (df_date['accident_year'] <= year_range[1])
    df_filtered = df_date[mask]

    columns = [{"name": i, "id": i} for i in df_filtered.columns]
    data = df_filtered.to_dict('records')
    # return '{}, {}, {}, {}, {}'.format(year_range, time_range, vehicle_no, start_date, end_date)
    return columns, data

# Create visualizations
# Simple bar chart
@app.callback(
    Output('loading-output-1', 'children'), # Loading indicator
    Output(simple_barchart.html_id, 'figure'),
    Input('year-filter-global', 'value') # dummy input, else callback doesn't work
)
def update_simple_barchart(value):
    return 'Barchart loaded', simple_barchart.update()



@app.callback(
    Output("map", "figure"),
    Input('year-filter-global', 'value')
)
def update_map(value):
    return make_map(df_location)


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')  # why debug not working :(
