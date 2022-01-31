from dash import dcc, html
import plotly.express as px


""""
    Creates a barchart.
"""

class StackedAreaChart(html.Div):
    def __init__(self, feature_x, feature_y, color, line_group, df, title):
        self.html_id = 'stacked-area-chart'
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y
        self.color = color
        self.line_group = line_group
        self.title= title
        self.update(self.color)

        # Equivalent to `html.Div([...])`
        super().__init__(
            html.Div(
                id='area-container',
                children=[
                    dcc.Graph(id=self.html_id, style={'height': '90%'},
                    figure=self.fig
                    ),
                    dcc.Dropdown(
                        id='area_select_dropdown',
                        style={'height': '10%'},
                        options=[
                            {'label': 'Weather conditions', 'value': 'weather_conditions'},
                            {'label': 'Maneuver type', 'value': 'vehicle_manoevre'}
                        ]
                    )
                ]
            )
        )

    def update(self, column):
        if column == 'weather_conditions':
            self.feature_y = 'count_weather'
            self.color = 'weather_conditions'
            self.title = 'Weather Conditions'
        elif column == 'vehicle_manoevre':
            self.feature_y = 'count_maneuver'
            self.color = 'vehicle_manoevre'
            self.title='Maneuver Type'
            
        self.fig = px.area(self.df
                            , x=self.feature_x
                            , y=self.feature_y
                            , color=self.color
                            , line_group=self.line_group
                            , title=self.title)
        return self.fig