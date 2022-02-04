from dash import html, dcc


"""
    The heatmap visualization class.
"""

class HeatMap():
    def __init__(self, range_filter_global_settings):
        self.max_year = range_filter_global_settings['maxYear']
        self.min_year = range_filter_global_settings['minYear']

    def get_heatmap(self):
        return html.Div([
            dcc.Graph(id='heatmap-graph', style={'height': '100%'}),
            ],
            style={'height': '100%'}
        )

    def get_heatmap_controls(self):
        return html.Div([
            html.H5('Heatmap controls'),
            html.Div([
                    dcc.Dropdown(
                        id='color',
                        options=[ {'label': 'Speed limit', 'value': 'speed'},
                                  {'label': 'Count of accidents', 'value': 'count' }],
                        value='count'
                    ),
                ], style={'width': '48%', 'display': 'inline-block', 'color': 'black'}
            )
            ]
        )
