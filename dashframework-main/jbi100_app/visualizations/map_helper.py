from geojson import Feature, FeatureCollection, Point, dump
import os

"""
    Helper file for the map visualization.
    Creates the geojson file that is needed to create the map.
"""

class Map_Helper():
    def __init__(self, data):
        # print(data)
        # print(data.iloc[0, 1])
        #
        # point = Point((data.iloc[0, 1], data.iloc[0, 2]))
        #
        # features = []
        # features.append(Feature(geometry=point, properties={'accident_index': str(data.iloc[0, 0])}))
        #
        # # add more features...
        # # features.append(...)
        #
        # feature_collection = FeatureCollection(features)
        #
        # with open('jbi100_app/assets/data/mapData.geojson', 'w') as f:
        #     dump(feature_collection, f)
        #
        # print('done')

        # data = data[:1000000]
        print('Started')

        features = []
        for index, row in data.iterrows():
            point = Point((row['longitude'], row['latitude']))

            feature = Feature(geometry=point, properties={'accident_index': str(row['accident_index'])}, id=index)
            features.append(feature)

        featureCollection = FeatureCollection(features)

        print('ended')
        # print(type(featureCollection))

        # save map file
        with open('jbi100_app/assets/data/mapData.geojson', 'w') as f:
            dump(featureCollection, f)

        print('saved')
