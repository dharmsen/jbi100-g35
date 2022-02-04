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
        self.update(self.color, self.df)

        # Equivalent to `html.Div([...])`
        super().__init__(
            html.Div(
                id='area-container',
                children=[
                    dcc.Graph(id=self.html_id, style={'height': '90%'},
                    figure=self.fig
                    )
                ]
            )
        )

    def create_dropdown(self):
        return html.Div(
            children=[
                html.H5('Stacked Area Chart'),
                dcc.Dropdown(
                    id='area_select_dropdown',
                    style={'height': '10%', 'color': 'black'},
                    options=[
                        {'label': 'Weather conditions', 'value': 'weather_conditions'},
                        {'label': 'Manoeuvre type', 'value': 'vehicle_manoeuvre'}
                    ],
                    value=self.color,
                    clearable=False,
                    searchable=False
                )
            ]
        )

    def update(self, column, df):
        if column == 'weather_conditions':
            self.feature_y = 'count_weather'
            self.color = 'weather_conditions'
            self.title = 'Weather Conditions'
        elif column == 'vehicle_manoeuvre':
            self.feature_y = 'count_manoeuvre'
            self.color = 'vehicle_manoeuvre'
            self.title= 'Manoeuvre Type'

        self.df = df
            
        self.fig = px.area(self.df
                            , x=self.feature_x
                            , y=self.feature_y
                            , color=self.color
                            , line_group=self.line_group
                            , title=self.title
                            , labels={self.feature_x: 'Year',
                            self.feature_y: 'Accident Count'})
        return self.fig
