import os.path

#Have to figure out which I use and which I dont use
import plotly.graph_objects as go
from geojson import load, FeatureCollection
import plotly.express as px
from .map_helper import Map_Helper
from dash import html, dcc

"""
    Creates a barchart visualization with built-in options for the x- and y-axis.
"""
class BarChart():
    # TODO 
    # apply years on dataframe -> such that it only shows the data of the year range
    # Apply No of vehicles involved on dataframe -> such that it only shows accidents were there were x amount of vehicles involved


    # TODO
    # Figure out what's happening here
    def __init__(self, xvalue, yvalue, df):
        #self.html_id = 'barchart-graph'
        self.df = df
        self.xvalue = xvalue
        self.yvalue = yvalue
        self.update(self.xvalue, self.yvalue, self.df)
        
        # Equivalent to `html.Div([...])`
        #super().__init__(
        #    dcc.Graph(id=self.html_id, style={'height': '100%'}),
        #    style={'height': '100%'}
        #)
        
    def get_barchart(self):
        return html.Div([
            dcc.Graph(id='barchart-graph', style={'height': '100%'}),
            ],
            style={'height': '100%'}
        )

    
    # Creates the dropdown to choose the value for x- and y-axis
    # TODO
    # Create dropdown for y-axis
    # Dropdown y-axis: {amount of accidents/ total amount of deaths/ average death per accident} 
    # Dropdown x-axis: {weather, maneuvres}
    def create_dropdown(self):
        return html.Div([
            html.Div([
                    dcc.Dropdown(
                        id='xaxis',
                        options=[ {'label': 'Weather conditions', 'value': 'weather_conditions'},
                                  {'label': 'Manoeuvre types', 'value': 'vehicle_manoeuvre' },
                                  {'label': 'Light conditions', 'value': 'light_conditions' },
                                  {'label': 'Road surface conditions', 'value': 'road_surface_conditions' },
                                  {'label': 'Special conditions at site', 'value': 'special_conditions_at_site' }],
                        #Default value: weather_conditions          
                        value='weather_conditions'
                    ),
                ], style={'width': '90%', 'display': 'inline-block', 'color': 'black', 'margin': 'auto'}
            ),
            html.Div([
                    dcc.Dropdown(
                        id='yaxis',
                        options=[ {'label': 'Amount of accidents', 'value': 'accident_index'},
                                  {'label': 'Total deaths', 'value': 'number_of_casualties' },
                                  {'label': 'Average deaths per accident', 'value': 'number_of_casualties_mean' },
                                  {'label': 'Median deaths per accident', 'value': 'number_of_casualties_median' }],
                        value='accident_index'
                    ),
                ], style={'width': '90%', 'display': 'inline-block', 'color': 'black', 'margin': 'auto'}
            )
            ], style = {'display': 'flex', 'flex-direction': 'column'}
        )
        
        
    
    
    # TODO
    # df_bar = df_barfilter
    def update(self, xvalue, yvalue, df_bar):
        # PROBLEM:
        # It only shows debug, i.e.xvalue and yvalue are most likely empty and therefore no graph will show up.
        
        # Giving the x lables corresponding to the xvalue
        # Else is for debug
        if xvalue == 'weather_conditions':
            self.lable_x = 'Weather Conditions'
        elif xvalue == 'vehicle_manoeuvre':
            self.lable_x= 'Manoeuvre Type'
        elif xvalue == 'light_conditions':
            self.lable_x= 'Light conditions'
        elif xvalue == 'road_surface_conditions':
            self.lable_x= 'Road surface conditions'
        elif xvalue == 'special_conditions_at_site':
            self.lable_x= 'Special conditions at site'
        else :
            xvalue = 'weather_conditions'
            self.lable_x = 'Debug: Weather Conditions'
        
        
        # yvalue2 = '' if yvalue corresponds with the correct column
        #   else yvalue2 = 'column_name'
        # Giving the y lables corresponding to the yvalue
        # Appointing the correct aggegrate functions based on the yvalue name
        if yvalue == 'accident_index':
            self.yvalue2 = ''
            self.lable_y = 'Total accidents'
            self.agg = 'count'
        elif yvalue == 'number_of_casualties':
            self.yvalue2 = ''
            self.lable_y = 'Total deaths'
            self.agg = 'count'
        elif yvalue == 'number_of_casualties_mean':
            self.yvalue2 = 'number_of_casualties'
            self.lable_y = 'Average deaths per accident'
            self.agg = 'mean'
        elif yvalue == 'number_of_casualties_median':
            self.yvalue2 = 'number_of_casualties'
            self.lable_y = 'Median deaths per accident'
            self.agg = 'median'
        else:
            self.yvalue2 = 'accident_index'
            self.lable_y = 'Debug: Total accidents'
            self.agg = 'count'


        # Update the groupby function according to the new x- and or y-value
        # Update the groupby function according the aggregate function
        if self.yvalue2 != "":
            self.df_groupedbybar = df_bar.groupby(xvalue).agg({self.yvalue2 : self.agg}).reset_index()
            self.fig = px.bar(self.df_groupedbybar,
                            x=xvalue, y=self.yvalue2, title='Barchart',
                            labels={xvalue: self.lable_x, self.yvalue2: self.lable_y})
        else:
            self.df_groupedbybar = df_bar.groupby(xvalue).agg({yvalue : self.agg}).reset_index()
            self.fig = px.bar(self.df_groupedbybar,
                            x=xvalue, y=yvalue, title='Barchart',
                            labels={xvalue: self.lable_x, yvalue: self.lable_y})
        
        # #Original, this works:
        # self.df_groupedbybar = df_bar.groupby('vehicle_manoeuvre').agg({'accident_index' : 'count'}).reset_index()    
        # self.fig = px.bar(self.df_groupedbybar,
                # x = "vehicle_manoeuvre", y = "accident_index",
                # labels={'accident_index': 'Total accidents', 'vehicle_manoeuvre': 'Manoeuvres'})
        
            
        
        return self.fig
