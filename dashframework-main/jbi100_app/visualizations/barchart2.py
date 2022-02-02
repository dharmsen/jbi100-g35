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
    def __init__(self, feature_x, feature_y, df, title):
        self.html_id = 'barchart-graph'
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y
        self.title= title
        self.update(self.df)
        
        # Equivalent to `html.Div([...])`
        super().__init__(
            dcc.Graph(id=self.html_id, style={'height': '100%'}),
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
                        options=[ {'label': 'Weather types', 'value': 'weather_conditions'},
                                  {'label': 'Manoeuvre types', 'value': 'vehicle_manoeuvre' }],
                        #Default value: weather_conditions          
                        value='weather_conditions'
                    ),
                ], style={'width': '48%', 'display': 'inline-block', 'color': 'black'}
            ),
            html.Div([
                    dcc.Dropdown(
                        id='yaxis',
                        options=[ {'label': 'Amount of accidents', 'value': 'accident_index'},
                                  {'label': 'Total deaths', 'value': 'number_of_casualties' },
                                  {'label': 'Average deaths per accident', 'value': 'number_of_casualties_mean' }],
                        value='accident_index'
                    ),
                ], style={'width': '48%', 'display': 'inline-block', 'color': 'black'}
            )
            ]
        )
        
        
        
        
    
    
    # TODO
    # When to use self. and when not?
    # Do I need to add self.yvalue or just yvalue?
    # DO I need self.yvalue2 or just yvalue2?
    def update(self, xvalue, yvalue, df_bar):
        # Giving the x lables corresponding to the xvalue
        if xvalue == 'weather_conditions':
            self.lable_x = 'Weather Conditions'
        elif xvalue == 'vehicle_manoeuvre':
            self.lable_x= 'Manoeuvre Type'
        
        
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


        # Update the groupby function according to the new x- and or y-value
        # Update the groupby function according the aggregate function
        if self.yvalue2 != "":
            df_groupedbybar = df_bar.groupby(self.xvalue).agg({self.yvalue2 : self.agg}).reset_index()
        else:
            df_groupedbybar = df_bar.groupby(self.xvalue).agg({self.yvalue : self.agg}).reset_index()
        
            
        self.fig = px.area(df_groupedbybar
                            , x=self.xvalue
                            , y=self.yvalue
                            , title='Barchart'
                            , labels={self.xvalue: self.label_x,
                            self.yvalue: self.label_y})
        return self.fig
