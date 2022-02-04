from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import Data
from jbi100_app.visualizations.barchart import Barchart
from jbi100_app.visualizations.map import Map_Visualization

from jbi100_app.visualizations.heatmap import HeatMap
from jbi100_app.visualizations.stackedareachart import StackedAreaChart


from jbi100_app.views.layout import generate_help_layout, generate_about_layout, generate_nav_bar, generate_basic_layout, generate_new_layout

from dash import html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import date

import dash_leaflet as dl

# Get data by making a data object and getting the required dfs from it.
# TODO: uncomment data object once in production, currently comment for quicker start up
# data = Data()
# df_date, df_conditions, df_location, df_severity = data.get_dataframes()

data = Data()

# FIXME: check imports
df_date, df_severity, df_conditions, df_location, df_heatmap, df_heatmap_speeds = data.get_dataframes()


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
df_map['hour_time'] = pd.to_datetime(df_map['time'], format='%H:%M').dt.hour


# Computes data points per year, used for ensuring not too many data points on map

years = list(df_map.drop_duplicates(subset=['accident_year'])['accident_year'])
yearCount = {}
for year in years:
    count = df_map[df_map['accident_year'] == year]['accident_year'].count()
    yearCount[year] = count


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

# Make heat map
heatmap = HeatMap(range_filter_global_settings)

# Make stacked area chart
df_merged_area_cond = df_date.join(df_conditions, lsuffix='_date', rsuffix='_conditions')
grouped_area_cond = df_merged_area_cond.groupby(['accident_year', 'weather_conditions']).size()
grouped_area_cond = grouped_area_cond.reset_index(name='count_weather')

df_merged_area_manu = df_date.join(df_severity, lsuffix='_date', rsuffix='_severity')
grouped_area_manu = df_merged_area_manu.groupby(['accident_year', 'vehicle_manoeuvre']).size()
grouped_area_manu = grouped_area_manu.reset_index(name='count_manoeuvre')

stacked_area_chart = StackedAreaChart('accident_year', 'count_weather', 'weather_conditions', None, grouped_area_cond, 'Weather Conditions')
# Declare visualizations
# vis is a tuple consiting of the visualization itself and the visualization object.

vis1 = (heatmap.get_heatmap(), heatmap)

vis2 = (map, m)

vis3 = ('vis3', 'obj')

# stacked_area_chart is implemented slightly differently so its technically both.
vis4 = (stacked_area_chart, stacked_area_chart)

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


def compute_size(startYear, endYear):
    total = 0
    years = list(range(startYear, endYear + 1))
    for year in years:
        total += yearCount[year]

    return total


def check_size_old(startYear, endYear):
    print('Running check_size_old')
    years = list(range(startYear, endYear + 1))
    total = compute_size(startYear, endYear)

    # print("Total at start: " + str(total))
    # If more than 500k reduce by 1 year and check again
    if total > 500000:
        # generate flipping pattern to cut list from front and back
        # cut from 0, -1, 1, -2, 2, -3, 3
        flipping = []
        for i in range(0, len(years)):
            if i == 0:
                flipping.append(i)
            else:
                flipping.append(i*-1)
                flipping.append(i)

        toRemove = []
        for i in flipping:
            if total > 500000:
                total -= yearCount[years[i]]
                toRemove.append(years[i])
            else:
                break

        # drop excess years
        for year in toRemove:
            years.remove(year)

        new_range = [years[0], years[1], total]
        print(new_range)
        return new_range

    print([startYear, endYear])
    return [startYear, endYear, total]


@app.callback(
    Output('map-info', 'children'),
    Output('map-info', 'style'),
    Output('map-tool-tip', 'style'),
    Input('map-range-slider', 'value')
)
def slider(value):
    # Size is approx from year counts
    size = compute_size(value[0], value[1])

    error_style_font = {'color': 'red'}
    error_style_visibility = {'visibility': 'visible', 'opacity': '1'}

    if size > 500000:
        return 'Data points loaded: EXCEEDED', error_style_font, error_style_visibility
    else:
        return 'Data points loaded: %s' % size, {}, {}


# Does actual map computing
@app.callback(
    Output('map', 'figure'),
    Output('loading-1-1', 'children'),
    Input('map-info', 'children'),
    Input('map-range-slider', 'value'),
    Input('time-filter-global', 'value'),
    Input('vehicles-slider-global', 'value'),
    Input('color-dropdown', 'value'),
    Input('size-dropdown', 'value'),
)
def do_map(txt, range, time_range, vehicle_no, color_drop, size_drop):
    print(time_range)
    if txt != 'Data points loaded: EXCEEDED':
        # 15 means 15 and more
        if vehicle_no == 15:
            vehicle_no = 1000

        df_map_filtered = df_map[(df_map['accident_year'] >= range[0]) &
                                 (df_map['accident_year'] <= range[1]) &
                                 (df_map['hour_time'] >= time_range[0]) &
                                 (df_map['hour_time'] <= time_range[1]) &
                                 (df_map['number_of_vehicles'] >= vehicle_no[0]) &
                                 (df_map['number_of_vehicles'] <= vehicle_no[1])
                                 ]
        print('Updating map!')

        return m.create_figure(df_map_filtered, color_drop, size_drop), ''
    else:
        # prevent update
        raise PreventUpdate


@app.callback(
    Output('map-hidden-panel', 'style'),
    Output('color-dropdown', 'options'),
    Output('size-dropdown', 'options'),
    Input('options-button', 'n_clicks')
)
def openOptions(value):

    # Get channel options for map
    columns = [
            {'label': 'Police Force', 'value': 'police_force'},
            {'label': 'Accident Severity', 'value': 'accident_severity'},
            {'label': 'Number of Vehicles', 'value': 'number_of_vehicles'},
            {'label': 'Deaths', 'value': 'number_of_casualties'},
            {'label': 'Day of Week', 'value': 'day_of_week'},
        ]


    # Makes pop up visible/ hidden
    if value is not None:
        if value % 2 == 1:
            return {'visibility': 'visible', 'opacity': '1'}, columns, columns

    return {'visibility' : 'hidden', 'opacity': '0'}, columns, columns


# Global filter callback function
@app.callback(
    Output('heatmap-graph', 'figure'), # heatmap output
    Output('map-range-slider', 'value'), # map range updater
    Input('year-filter-global', 'value'),
    Input('time-filter-global', 'value'),
    Input('vehicles-slider-global', 'value'),
    # Input('date-picker-global', 'start_date'),
    # Input('date-picker-global', 'end_date'),
    # Input('year_slider', 'value'),
    Input('color', 'value')
)
def global_filter(year_range, time_range, vehicle_no, heatmap_color):
    # global year range is used right now
    print('hello')
    heatmap = update_figure(year_range, heatmap_color)

    map_range = check_size_old(year_range[0], year_range[1])[:2]

    return heatmap, map_range

# Heatmap updater
def update_figure(value, color):
    if color == 'count':
        filtered_df = df_heatmap[(df_heatmap['accident_year'] <= value[1]) & (df_heatmap['accident_year'] >= value[0])]
        filtered_df = filtered_df.pivot_table('count', 'accident_year', 'weekNum')
    else:
        filtered_df = df_heatmap_speeds[(df_heatmap_speeds['accident_year'] <= value[1]) & (df_heatmap_speeds['accident_year'] >= value[0])]
        filtered_df = filtered_df.pivot_table('speed_limit', 'accident_year', 'weekNum')

    fig = px.imshow(filtered_df,color_continuous_scale=px.colors.sequential.Bluyl, title='Heat Map')
    fig.update_yaxes(title='Accident Year')
    fig.update_xaxes(title='Week number')
    if(color == "count"):
        fig.update_traces(hoverongaps=False,
                      hovertemplate="Accident Year: %{y}"
                                    "<br>Week number: %{x}"
                                    "<br>Number of accidents: %{z}<extra></extra>"
                      )
    else:
        fig.update_traces(hoverongaps=False,
                  hovertemplate="Accident Year: %{y}"
                                "<br>Week number: %{x}"
                                "<br>Average Speed Limit: %{z}<extra></extra>"
                  )
    fig.update_layout(transition_duration=500, margin=dict(l=5, r=5, t=35, b=5))
    return fig


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

