from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import Data
from jbi100_app.visualizations.barchart import Barchart
from jbi100_app.visualizations.stackedareachart import StackedAreaChart

from jbi100_app.views.layout import generate_help_layout, generate_about_layout, generate_nav_bar, generate_basic_layout, generate_new_layout

from dash import html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from datetime import date



# Get data by making a data object and getting the required dfs from it.
# TODO: uncomment data object once in production, currently comment for quicker start up
# data = Data()
# df_date, df_conditions, df_location, df_severity = data.get_dataframes()

data = Data()
df_date, df_severity, df_conditions = data.get_dataframes()

# FIXME: accident_index col is killing the table
df_date.drop('accident_index', inplace=True, axis=1)

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


# Make simple barchart vis example
# Join together for barchart
df_merged = df_date.join(df_severity, lsuffix='_date', rsuffix='_severity')
grouped = df_merged.groupby('accident_year').agg({'number_of_casualties': 'mean'})
grouped = grouped.reset_index()

simple_barchart = Barchart('accident_year', 'number_of_casualties', grouped)

# Make stacked area chart
df_merged_area_cond = df_date.join(df_conditions, lsuffix='_date', rsuffix='_conditions')
grouped_area_cond = df_merged_area_cond.groupby(['accident_year', 'weather_conditions']).size()
grouped_area_cond = grouped_area_cond.reset_index(name='count_weather')

df_merged_area_manu = df_date.join(df_severity, lsuffix='_date', rsuffix='_severity')
grouped_area_manu = df_merged_area_manu.groupby(['accident_year', 'vehicle_manoeuvre']).size()
grouped_area_manu = grouped_area_manu.reset_index(name='count_manoeuvre')

stacked_area_chart = StackedAreaChart('accident_year', 'count_weather', 'weather_conditions', None, grouped_area_cond, 'Weather Conditions')
# Declare visualizations
vis1 = 'vis1'

vis2 = 'vis2'

vis3 = 'vis3'

vis4 = stacked_area_chart

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="main",
            children=[
                generate_nav_bar(),
                # main div that holds all content
                html.Div(
                    id='vis-main'
                )
            ]
        ),
    ],
)

main_page_layout = generate_new_layout(range_filter_global_settings, date_filter_global_settings, vis1, vis2, vis3, vis4)
#
#
about_layout = generate_about_layout()
help_layout = generate_help_layout()
#
# Update the index
@app.callback(Output('vis-main', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/about':
        return about_layout
    elif pathname == '/help':
        return help_layout
    elif pathname == '/':
        return main_page_layout
    else:
        # handle not known URL
        return html.H1("Error 404: page not found.", style={'color': 'red'})


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
# @app.callback(
#     Output('loading-output-1', 'children'), # Loading indicator
#     Output(simple_barchart.html_id, 'figure'),
#     Input('year-filter-global', 'value') # dummy input, else callback doesn't work
# )

# def update_simple_barchart(value):
#     return 'Barchart loaded', simple_barchart.update()

# Stacked bar chart
@app.callback(
    Output('stacked-area-chart', 'figure'),
    Input('year-filter-global', 'value'),
    Input('area_select_dropdown', 'value')
)

def update_stacked_area_chart(value, area_select_dropdown):
    if area_select_dropdown == 'weather_conditions':
        return stacked_area_chart.update(area_select_dropdown, grouped_area_cond)
    elif area_select_dropdown == 'vehicle_manoeuvre':
        return stacked_area_chart.update(area_select_dropdown, grouped_area_manu)


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')  # why debug not working :(
