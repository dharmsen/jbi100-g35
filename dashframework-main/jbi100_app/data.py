import plotly.express as px
import pandas as pd
import os

""""
    Data processor class. Does all the data parsing and preprocessing. Returns any  required settings for filters.
"""
class Data:

    # All data frames are initialized inside the constructor.
    def __init__(self):

        # all data lives here
        DATA_PATH = 'jbi100_app/assets/data/'

        # Check if parquet files already exist
        if os.path.exists(DATA_PATH + 'location.parquet') and \
                os.path.exists(DATA_PATH + 'date.parquet') and \
                os.path.exists(DATA_PATH + 'conditions.parquet') and \
                os.path.exists(DATA_PATH + 'severity.parquet'):

            print('Parquet files located, creating dataframes...')

            # TODO: commented for quicker start up
            # self.df_conditions = pd.read_parquet(DATA_PATH + 'conditions.parquet')
            self.df_date = pd.read_parquet(DATA_PATH + 'date.parquet')
            # self.df_location = pd.read_parquet(DATA_PATH + 'location.parquet')
            self.df_severity = pd.read_parquet(DATA_PATH + 'severity.parquet')

        else:
            # If files are missing, must create them

            print('Parquet files missing, creating parquet files...')

            self.df = pd.read_csv(DATA_PATH +
                                  'dft-road-casualty-statistics-accident-1979-2020.csv')

            self.df_nonull = self.df.dropna()

            self.df_nonull['accident_index'] = self.df_nonull['accident_index'].str.encode('utf-8')

            self.df_location = self.df_nonull[['accident_index', 'longitude', 'latitude']]

            self.df_date = self.df_nonull[['accident_index', 'accident_year', 'date', 'day_of_week', 'time']]

            self.df_conditions = self.df_nonull[
                ['accident_index', 'light_conditions', 'weather_conditions', 'road_surface_conditions',
                 'special_conditions_at_site']]

            self.df_severity = self.df_nonull[
                ['accident_index', 'police_force', 'accident_severity', 'number_of_vehicles', 'number_of_casualties']]

            self.df_location.to_parquet('{}location.parquet'.format(DATA_PATH), engine='fastparquet')
            self.df_date.to_parquet('{}date.parquet'.format(DATA_PATH), engine='fastparquet')
            self.df_conditions.to_parquet('{}conditions.parquet'.format(DATA_PATH), engine='fastparquet')
            self.df_severity.to_parquet('{}severity.parquet'.format(DATA_PATH), engine='fastparquet')

    # Returns the four dataframes: conditions, date, location, severity
    def get_dataframes(self) -> pd.DataFrame:
        # TODO: commented for performance increase
        return self.df_date, self.df_severity, self.df_conditions#, self.df_location

    # Returns settings for slider, like mins and maxes
    def get_range_filter_global_settings(self) -> dict:
        return {
            'minYear': min(self.df_date['accident_year']),
            'maxYear': max(self.df_date['accident_year']),
        }

    # Returns settings for date picker
    def get_date_filter_global_settings(self) -> dict:
        return {
            'minDate': min(self.df_date['date']),
            'maxDate': max(self.df_date['date'])
        }
