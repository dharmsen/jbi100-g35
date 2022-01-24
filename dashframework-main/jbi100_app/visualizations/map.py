import os.path

import plotly.graph_objects as go
from geojson import load, FeatureCollection
import plotly.express as px
from .map_helper import Map_Helper
from dash import html, dcc


"""
    Creates a map visualization with built-in year slider to limit data points.
"""
class Map_Visualization():

    def __init__(self, data, range_filter_global_settings):
        # TODO: set this as a global variable
        DATA_PATH = 'jbi100_app/assets/data/'

        # TODO: decide if will use other map type with geojson
        # Check if geojson file exists
        # if (os.path.exists(DATA_PATH + 'mapData.geojson'))
        # geojson = Map_Helper(data)

        # create figure
        self.fig = self.create_figure(data)
        self.range_filter_global_settings = range_filter_global_settings


    def create_figure(self, data):
        fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color='number_of_vehicles',
                                size='number_of_casualties',
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=2)

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
                dcc.Graph(id='map', style={'height': '100%'}, figure=self.fig),
                dcc.RangeSlider(
                    id='map-range-slider',
                    min=self.range_filter_global_settings['minYear'],
                    max=self.range_filter_global_settings['maxYear'],
                    step=2,

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
                    value=[2019, 2020]
                )
            ]
        )


