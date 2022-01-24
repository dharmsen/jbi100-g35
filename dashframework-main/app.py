from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import Data
from jbi100_app.visualizations.barchart import Barchart
from jbi100_app.visualizations.map import Map_Visualization

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

df_map = df_location.join(df_severity, rsuffix='_b')
df_map = df_map.join(df_date, rsuffix='_c')

print(df_map.columns)

# 500,000 nominal performance (probably best to stay here to ensure resources are left for other visualizations)
# 750,000 not great performance
# 1mil quite laggy
# 3.7mil crashes (all rows)
print('Starting map')
# TODO configure best starting values
m = Map_Visualization(df_map[(df_map['accident_year'] >= 2019) & (df_map['accident_year'] <= 2020)], range_filter_global_settings)
map = m.get_map_vis()
print('Map finished')



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
                generate_new_layout(range_filter_global_settings, date_filter_global_settings, simple_barchart, map)
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

# Map callbacks
@app.callback(
    Output('map', 'figure'),
    Input('map-range-slider', 'value')
)
def update_map(value):
    # Filter copy of df_map for given dates
    print('Year 1: ' + str(value[0]))
    print('Year 2: ' + str(value[1]))
    df_map_filtered = df_map[(df_map['accident_year'] >= value[0]) & (df_map['accident_year'] <= value[1])]

    # TODO: figure out how to only render 500k rows max, maybe save number of rows for each year and
    #  # TODO: then quick dictionary look up to make sure total is less than 500k, else just set year to next one up avoiding exceeding 500k

    # TODO: add loading icon
    return m.create_figure(df_map_filtered)


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')  # why debug not working :(
