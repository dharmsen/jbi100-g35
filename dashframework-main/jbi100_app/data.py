import plotly.express as px
import pandas as pd

""""
    Data processor class. Does all the data parsing and preprocessing.
"""

class Data:

    # All data frames are initialized inside the constructor.
    def __init__(self):

        # Removed the link to internet since it was taking 5 business days to do anything
        self.df = pd.read_csv(
            "dft-road-casualty-statistics-accident-1979-2020.csv")

        self.df_nonull = self.df.dropna()

        self.df_nonull['accident_index'] = self.df_nonull['accident_index'].str.encode('utf-8')

        self.df_location = self.df_nonull[['accident_index', 'longitude', 'latitude']]

        self.df_date = self.df_nonull[['accident_index', 'accident_year', 'date', 'day_of_week', 'time']]

        self.df_conditions = self.df_nonull[
            ['accident_index', 'light_conditions', 'weather_conditions', 'road_surface_conditions',
             'special_conditions_at_site']]

        self.df_severity = self.df_nonull[['accident_index', 'police_force', 'accident_severity', 'number_of_vehicles',
                                 'number_of_casualties']]

        self.df_location.to_parquet('location.parquet', engine='fastparquet')
        self.df_date.to_parquet('date.parquet', engine='fastparquet')
        self.df_conditions.to_parquet('conditions.parquet', engine='fastparquet')
        self.df_severity.to_parquet('severity.parquet', engine='fastparquet')
