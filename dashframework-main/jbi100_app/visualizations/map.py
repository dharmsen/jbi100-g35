import os.path

import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc


"""
    Creates a map visualization with built-in year slider to limit data points.
    
    Performance notes:
    500,000 nominal performance (probably best to stay here to ensure resources are left for other visualizations)
    750,000 not great performance
    1mil quite laggy
    3.7mil crashes (all rows)
"""
class Map_Visualization():

    def __init__(self, data, range_filter_global_settings, yearCount):
        # TODO: set this as a global variable
        DATA_PATH = 'jbi100_app/assets/data/'

        # TODO: decide if will use other map type with geojson
        # Check if geojson file exists
        # if (os.path.exists(DATA_PATH + 'mapData.geojson'))
        # geojson = Map_Helper(data)

        # create figure
        self.fig = self.create_figure(data, 'number_of_vehicles', 'number_of_casualties')
        self.range_filter_global_settings = range_filter_global_settings

        self.yearCount = yearCount


    def create_figure(self, data, color, size):

        fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color=color,
                                size=size,
                                hover_data= {size: True,
                                             color: True,
                                             'time': True,
                                             'date': True
                                             },
                                labels={'police_force': 'Police Force',
                                        'accident_severity': ' Accident Severity',
                                        'number_of_vehicles': 'Number Of Vehicles',
                                        'number_of_casualties': 'Deaths',
                                        'day_of_week': 'Day Of Week',
                                        'Latitude': 'latitude',
                                        'Longitude': 'longitude',
                                        'Time': 'time',
                                        'Date': 'date',
                                        },
                                color_continuous_scale=px.colors.sequential.thermal, size_max=15, zoom=2)

        # update fig
        self.update_fig(fig)


        return fig

    def update_fig(self, fig):
        fig.update_layout(
            mapbox_style="open-street-map",
            margin=dict(l=5, r=5, t=5, b=5),
        )



    """
        Returns div containing map vis with built in year slider.
        This vis has a seperate year slider to improve performance.
    """
    def get_map_vis(self):
        return html.Div(
            id='map-container',
            children=[
                # dummy input to have loading screen
                # dcc.Input(id="loading-input-1-1",
                #           value='Input triggers local spinner',
                #           style={'visibility': 'hidden',
                #                  'position': 'absolute'}),
                # dcc.Loading(
                #     id="loading-1-1",
                #     type="default",
                #     style={'height': '100%'},
                #     children=dcc.Graph(id='map', style={'height': '100%'},
                #                        figure=self.fig),
                # ),
                dcc.Graph(id='map', style={'height': '100%'},
                          figure=self.fig),

                # self.generate_controls()
                # fix CSS here
                # rows indicator
                html.Div(
                    id='map-info-wrapper',
                    children=[
                        html.Div(
                            id='map-info-panel',
                            children=[
                                # displays: Data points loaded: XXX
                                html.P(
                                    id='map-info',
                                    children=['Data points loaded: '])
                            ]
                        ),
                        # loading indicator
                        html.Div(
                            id='loading-wrapper',
                            children=
                            dcc.Loading(
                                id="loading-1-1",
                                type="default",
                                style={'height': '50%'},
                            ),
                        )
                    ]
                )
            ]
        )


    def generate_controls(self):
        # Define controls for map vis in this div
        return html.Div(children=[html.H5('Map controls'),
            html.Div(
            id='map-control-panel',
            children=[
                dcc.RangeSlider(
                    id='map-range-slider',
                    min=self.range_filter_global_settings['minYear'],
                    max=self.range_filter_global_settings['maxYear'],
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},

                    # TODO: figure out how to only have a max distance of 3 between both handles
                    marks={
                        str(self.range_filter_global_settings['minYear']): {'label':
                                                                                self.range_filter_global_settings[
                                                                                    'minYear'],
                                                                            'style': {'color': '#fff'}},
                        str(self.range_filter_global_settings['maxYear']): {'label':
                                                                                self.range_filter_global_settings[
                                                                                    'maxYear'],
                                                                            'style': {'color': '#fff'}},
                    },
                    value=[2019, 2020],
                ),
                html.Div(
                  id='map-tool-tip',
                  children=['Your current selection exceeds the performance '
                            'capabilites of this map. Please make a smaller '
                            'choice.']
                ),
                # Options drop down
                html.Div(
                    id='map-options',
                    children=[
                        html.Button(
                            id='options-button',
                            className='btn btn-primary',
                            style={'color': '#fff'},
                            children=[
                                html.Div(
                                    className='button-wrapper',
                                    children=[
                                        html.P('Options'),
                                        html.Img(
                                            className='drop-icon',
                                            src="/assets/bootstrap-icons-1.7.2/caret-down-square.svg",
                                            alt="Drop down icon",
                                        ),
                                    ]
                                )
                            ],
                        ),
                        html.Div(
                            id='map-hidden-panel',
                            children=[
                                html.P('Choose which channels represent what data'),
                                html.Div(
                                    className='drop-down-label',
                                    children=[
                                        html.P('Color: '),
                                        dcc.Dropdown(
                                            id='color-dropdown',
                                            value='number_of_vehicles',
                                            style={'width': '100%', 'color': 'black'}
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='drop-down-label',
                                    children=[
                                        html.P('Size: '),
                                        dcc.Dropdown(
                                            id='size-dropdown',
                                            # default value
                                            value='number_of_casualties',
                                            style={'width': '100%', 'color': 'black'}
                                        )
                                    ]
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
        ])


    def check_size_old(self, startYear, endYear):
        years = list(range(startYear, endYear + 1))
        total = self.compute_size(startYear, endYear)

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
                    flipping.append(i * -1)
                    flipping.append(i)

            toRemove = []
            for i in flipping:
                if total > 500000:
                    total -= self.yearCount[years[i]]
                    toRemove.append(years[i])
                else:
                    break

            # drop excess years
            for year in toRemove:
                years.remove(year)

            new_range = [years[0], years[1], total]
            return new_range

        return [startYear, endYear, total]

    def compute_size(self, startYear, endYear):
        total = 0
        years = list(range(startYear, endYear + 1))
        for year in years:
            total += self.yearCount[year]

        return total