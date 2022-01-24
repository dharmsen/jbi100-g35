import os.path

import plotly.graph_objects as go
from geojson import load, FeatureCollection
import plotly.express as px
import random
from .map_helper import Map_Helper

def make_map(data):

    # TODO: set this as a global variable
    DATA_PATH = 'jbi100_app/assets/data/'

    # Check if geojson file exists
    # if (os.path.exists(DATA_PATH + 'mapData.geojson'))
    # geojson = Map_Helper(data)

    # with open('jbi100_app/assets/data/mapData.geojson') as f:
    #     collection = load(f)

    #collection = load('jbi100_app/assets/data/mapData.geojson')

    # print(collection)
    print(len(data))
    data = data[:500000]
    data['test'] = random.randrange(10)
    data['new_index'] = str(data['accident_index'])

    # fig = px.density_mapbox(data, lat='latitude', lon='longitude', z='test', radius=10,
    #                         center=dict(lat=0, lon=180), zoom=0,
    #                         mapbox_style="stamen-terrain")
    # fig.show()

    # fig = px.choropleth(data, geojson=collection, color="test",
    #                     locations="new_index", featureidkey="properties.accident_index",
    #                     )
    # fig.update_geos(fitbounds="locations", visible=False)
    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # fig.show()

    # px.set_mapbox_access_token(open(".mapbox_token").read())

    # df = px.data.carshare()
    # fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", size="test", #color="blue",
    #                         color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
    #
    # fig.update_layout(
    #     mapbox_style="open-street-map",
    # )

    data['size'] = 5
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color='number_of_vehicles', size='number_of_casualties',#color='number_of_casualties', size='number_of_vehicles',
                            color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

    # fig = go.Figure(go.Scattermapbox(
    #     lat=data["latitude"],
    #     lon=data["longitude"],
    #     mode="markers+text",
    #     marker={"size": 10},
    #     ))
    #
    fig.update_layout(
        mapbox_style="open-street-map",
    )

    fig.show()
    return fig