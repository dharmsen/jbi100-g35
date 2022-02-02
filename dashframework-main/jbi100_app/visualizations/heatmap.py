from dash import html, dcc


"""
    The heatmap visualization class.
"""

class HeatMap():
    def __init__(self, min_year, max_year):
        self.max_year = max_year
        self.min_year = min_year

    def get_heatmap(self):
        return html.Div([
            dcc.Graph(id='heatmap-graph', style={'height': '100%'}),
            ],
            style={'height': '100%'}
        )

    def get_heatmap_controls(self):
        return html.Div([
            html.Div([
                    dcc.Dropdown(
                        id='color',
                        options=[ {'label': 'Speed limit', 'value': 'speed'},
                                  {'label': 'Count of accidents', 'value': 'count' }],
                        value='count'
                    ),
                ], style={'width': '48%', 'display': 'inline-block', 'color': 'black'}
            ),
            dcc.RangeSlider(
                id='year_slider',
                min=self.min_year,
                max=self.max_year,
                value=[self.min_year, self.max_year],
                step=1,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            ]
        )
