from dash import dcc, html
import plotly.express as px


""""
    Creates a barchart.
"""

class Barchart(html.Div):
    def __init__(self, feature_x, feature_y, df):
        self.html_id = 'basic-barchart'
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            dcc.Graph(id=self.html_id, style={'height': '100%'}),
            style={'height': '100%'}
        )

    def update(self):
        self.fig = px.bar(self.df, x=self.feature_x, y=self.feature_y, title='Simple Bar Chart')
        return self.fig
