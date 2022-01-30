from dash import dcc, html
import plotly.express as px


""""
    Creates a barchart.
"""

class StackedAreaChart(html.Div):
    def __init__(self, feature_x, feature_y, color, line_group, df):
        self.html_id = 'stacked-area-chart'
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y
        self.color = color
        self.line_group = line_group

        # Equivalent to `html.Div([...])`
        super().__init__(
            dcc.Graph(id=self.html_id, style={'height': '100%'}),
            style={'height': '100%'}
        )

    def update(self):
        self.fig = px.area(self.df
                            , x=self.feature_x
                            , y=self.feature_y
                            , color=self.color
                            , line_group=self.line_group
                            , title='Stacked Area Chart')
        return self.fig
