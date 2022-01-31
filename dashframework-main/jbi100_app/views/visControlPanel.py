from dash import dcc, html
from jbi100_app.main import app
from dash.dependencies import Input, Output
from datetime import date

from jbi100_app.visualizations.heatmap import HeatMap


# Stores visualization control panels that pop up when user hovers over vis icons.

# Generates the control panel that appears when user hovers over vis icons.
def generate_control_panel(visId: int):
    # TODO: add custom behaviour depending on visId

    # Not the best since hardcoding each position for each vis
    controls = 'Controls go here.'
    if visId == 1:
        heatmap = HeatMap(1979, 2020)
        controls = heatmap.get_heatmap_controls()

    return html.Span(
        className="tooltiptext",
        children=[
            html.Div(
                className="div-inside-span",
                children=[
                    controls
                ]
            )
        ]
    )


# Global filtering control panel
def generate_global_control_panel(range_filter_global_settings, date_filter_global_settings):
    return html.Span(
        className="tooltiptext",
        children=[
            html.Div(
                className='div-inside-span',
                children=[
                    html.H5(className='filter-title', children=['Global Filters']),
                    # Date range slider
                    html.Div(
                        className='container',
                        children=[
                            html.P(className='filter-title-global', children=['Year Range: ']),
                            dcc.RangeSlider(
                                className='filter-global',
                                id='year-filter-global',
                                min=range_filter_global_settings['minYear'],
                                max=range_filter_global_settings['maxYear'],
                                step=1,
                                value=[range_filter_global_settings['minYear'],
                                       range_filter_global_settings['maxYear']],
                                marks={
                                    str(range_filter_global_settings['minYear']): {'label':
                                                                                       range_filter_global_settings[
                                                                                           'minYear'],
                                                                                   'style': {'color': '#fff'}},
                                    str(range_filter_global_settings['maxYear']): {'label':
                                                                                       range_filter_global_settings[
                                                                                           'maxYear'],
                                                                                   'style': {'color': '#fff'}},
                                },
                                allowCross=False,
                            ),

                        ]
                    ),

                    # Time range slider
                    html.Div(
                        className='container',
                        children=[
                            html.P(className='filter-title-global', children=['Time Range: ']),
                            dcc.RangeSlider(
                                className='filter-global',
                                id='time-filter-global',
                                min=0,
                                max=24,
                                step=1,
                                value=[0, 24],
                                marks={
                                    0: {'label': '00:00', 'style': {'color': '#fff'}},
                                    12: {'label': '12:00', 'style': {'color': '#fff'}},
                                    24: {'label': '24:00', 'style': {'color': '#fff'}},
                                },
                                allowCross=False,
                            ),

                        ]
                    ),

                    # No. of vehicles slider
                    html.Div(
                        className='container',
                        children=[
                            html.P(className='filter-title-global', children=['No. of Vehicles: ']),
                            dcc.Slider(
                                className='filter-global',
                                id='vehicles-slider-global',
                                min=1,
                                max=10,
                                step=1,
                                value=[1, 10],
                                marks={
                                    1: {'label': '1', 'style': {'color': '#fff'}},
                                    5: {'label': '5', 'style': {'color': '#fff'}},
                                    10: {'label': '10+', 'style': {'color': '#fff'}},
                                },
                            ),

                        ]
                    ),

                    # Date picker
                    html.Div(
                        className='container',
                        children=[
                            html.P(className='filter-title-global', children=['Dates: ']),
                            dcc.DatePickerRange(
                                className='filter-global',
                                id='date-picker-global',
                                min_date_allowed=date_filter_global_settings['minDate'],
                                max_date_allowed=date_filter_global_settings['maxDate'],
                            ),
                        ]
                    )
                ]
            )
        ]
    )