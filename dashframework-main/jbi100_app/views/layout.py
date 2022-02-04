from dash import dcc, html
from jbi100_app.views.visControlPanel import generate_control_panel, generate_global_control_panel
from jbi100_app.main import app
from dash.dependencies import Input, Output

""""
    Stores some components for layout
"""


# Returns a nav bar
def generate_nav_bar():
    return html.Div(
        id="nav-bar",
        children=[
            html.Ul(
                children=[
                    # TODO: link anchors to pages
                    dcc.Location(id='url', refresh=False),

                    # dcc.Link('Navigate to "/"', href='/'),
                    html.Li(
                        children=[
                            dcc.Link('Homepage', href='/'),
                            # html.A(
                            #     children=["Homepage"], href="#")
                        ]
                    ),
                    # html.Li(
                    #     children=[
                    #         dcc.Link('Navigate to "/"', href='/'),
                    #         # html.A(
                    #         #     children=["Visualizations"], href="#")
                    #     ]),
                    html.Li(
                        children=[
                            dcc.Link('About', href='/about'),
                            # html.A(
                            #     children=["About"], href="#")
                        ]),
                    html.Li(
                        children=[
                            dcc.Link('Help', href='/help'),
                            # html.A(
                            #     children=["Help"], href="#")
                        ]),
                ]
            )
        ]
    )


def generate_basic_layout():
    return html.Div(
        id="vis",
        children=[
            html.Div(
                id="vis-controls",
                children=[
                    html.H4(children=["Visualization Controls"])
                    # TODO: add some controls here
                ]
            ),
            html.Div(
                id="vis-container",
                children=[
                    html.H4(children=["Visualizations"])
                    # TODO: vis goes here
                ]
            )
        ],
    )

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Each visualization is assigned a unique id that informs drawer what items are needed inside the control panel
def generate_hover_over_control_panel(visId: int, vis):
    vis_names = ['Heatmap', 'Map', 'Bar chart', 'Stacked area Chart']

    return html.Div(
        className="tooltip",
        children=[
            html.Img(
                className='picture',
                # src="/assets/bootstrap-icons-1.7.2/clipboard-data.svg",
                src="/assets/bootstrap-icons-1.7.2/file-earmark-bar-graph.svg",
                alt="Vis icon",
                width="64",
                height="64"
            ),
            html.P('Filter {}'.format(vis_names[visId-1])),
            generate_control_panel(visId, vis)
        ]
    )


# Generates a panel that globally filters that dataset
def generate_global_filtering_panel(range_filter_global_settings, date_filter_global_settings):
    return html.Div(
        className='tooltip',
        id='global-filter',
        children=[
            html.Img(
                # src="/assets/bootstrap-icons-1.7.2/clipboard-data.svg",
                src="/assets/bootstrap-icons-1.7.2/globe.svg",
                alt="Globe icon",
                width="64",
                height="64"
            ),
            html.P('Global Filters'),
            generate_global_control_panel(range_filter_global_settings, date_filter_global_settings)
        ]
    )

# Generates the side bar for main page
def generate_side_bar(range_filter_global_settings, date_filter_global_settings, vis1, vis2, vis3, vis4):
    return html.Div(
        id='side-bar',
        children=[
            # TODO: add spinner to better place
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div(id="loading-output-1")
            ),
            generate_global_filtering_panel(range_filter_global_settings, date_filter_global_settings),
            generate_hover_over_control_panel(1, vis1),
            generate_hover_over_control_panel(2, vis2),
            generate_hover_over_control_panel(3, vis3),
            generate_hover_over_control_panel(4, vis4)
        ]
    )

# Generates visualization container for main page
def generate_vis_container(vis1, vis2, vis3, vis4):

    return html.Div(
        id="vis-new-container",
        children=[
            html.Div(
                className="visBox",
                id="vis1",
                children=[vis1]
            ),
            html.Div(
                className="visBox",
                id="vis2",
                children=[vis2]
            ),
            html.Div(
                className="visBox",
                id="vis3",
                children=[vis3]
            ),
            html.Div(
                className="visBox",
                id="vis4",
                children=[vis4]
            ),
        ]
    )


def generate_new_layout(range_filter_global_settings, date_filter_global_settings, vis1, vis2, vis3, vis4):
    return html.Div(
        id="vis",
        children=[
            generate_side_bar(range_filter_global_settings, date_filter_global_settings, vis1[1], vis2[1], vis3[1], vis4[1]),
            generate_vis_container(vis1[0], vis2[0], vis3[0], vis4[0])
        ]
    )


def generate_about_layout():
    return html.Div(
        className='aux-pages',
        id='about-main',
        children=[
            html.H1('About page'),
            html.P('Here you can find some info about each of the visualizations.'),
            html.Div(
                id='about-container',
                children=[
                    html.Div(
                        id='about-card',
                        children=[
                            html.H3('Barchart Visualization'),
                            html.Img(
                                src='/assets/barPicture.PNG',
                                alt='Image of bar chart',
                                className='about-image'),
                            html.P(
                                'A bar-chart makes use of a quantitative and qualitative variable. The bar-chart '
                                'shows what certain variables have an influence on the amount of accidents, the '
                                'amount of death in an accident, the average death per accident, and the median '
                                'death per accident. Variables that could be chosen to see the influence of on these'
                                ' factors include: weather conditions, manoeuvre types, light conditions, road surface '
                                'conditions, and special conditions at site.'
                            )
                        ]
                    ),
                    html.Div(
                        id='about-card',
                        children=[
                            html.H3('Heatmap Visualization'),
                            html.Img(
                                src='/assets/heatmapPicture.PNG',
                                alt='Image of heatmap',
                                className='about-image'),
                            html.P(
                                'The heatmap is built in the style of the yearly calendar. presenting years on'
                                'they-axis and weeks on the x-axis allows the user to navigate both ways to search'
                                'for patterns. The visualization has two filters. The range slider for the selection'
                                'of years is providing the freedom of exploration and in-depth analysis if needed.'
                                'In addition, the coloring of the heatmap is determined by a second filter - count '
                                'of an accident or the average speed limit of vehicles from the accidents. Lighter'
                                'colors indicate a smaller number while the dark ones are close to maximum.'
                            )
                        ]
                    ),
                    html.Div(
                        id='about-card',
                        children=[
                            html.H3('Stacked Area Visualization'),
                            html.Img(
                                src='/assets/areaPicture.PNG',
                                alt='Image of stacked area chart',
                                className='about-image'),
                            html.P(
                                'The stacked area chart shows the distribution and amount of accidents between several' 
                                ' categories over time. The categories are manoeuvre types and weather conditions. This' 
                                ' visualization can be used to see the general trend and the trend per category over the'
                                ' course of a timeframe.'
                            )
                        ]
                    ),
                    html.Div(
                        id='about-card',
                        children=[
                            html.H3('Map Visualization'),
                            html.Img(
                                src='/assets/mapPicture.PNG',
                                alt='Image of map vis',
                                className='about-image'
                            ),
                            html.P(
                                'The map visualization visualizes the provided spatial data and allows the user '
                                'to identify cities and roads with large amounts of accidents. The map supports all'
                                ' standard interaction techniques like panning and zooming. The user can also hover'
                                ' over particular accident sites to see more details. Apart from the spatial data, the'
                                ' map encodes different attributes via color and size of the dots on the map. These '
                                'attributes can be changed by clicking the options button. To ensure consistent '
                                'performance the map is limited to rendering under half a million datapoints and the '
                                'user is informed when this limit is exceeded. '
                            )
                        ]
                    )
                ]
            ),
            html.P('Created by Group 37 for JBI100 at TUE. Generation 2021-2022.')
        ]
    )

def generate_help_layout():
    return html.Div(
        className='aux-pages',
        id='about-help',
        children=[
            html.H1('Help page'),
            html.P('Here you can find some help information for each of the visualizations.'),
            html.Div(
                id='help-container',
                children=[
                    html.Div(
                        id='help-card',
                        children=[
                            html.H3('General Help'),
                            html.P('All visualizations support multiple interaction techniques. Some of them are: '
                                   'panning, zooming and filtering. To zoom, simply use your mouse scroll wheel or use '
                                   'the zoom controls in the top right corner of each figure. To pan, simply drag the '
                                   'figure where you’d like to go. Where panning is not supported, dragging instead '
                                   'creates a selection to zoom in on in the visualization. Filtering can be applied '
                                   'at both a global level that filters the whole dataset so that all visualizations '
                                   'show a filtered subset of the original data or at a local level where only that '
                                   'visualization shows a subset of the original data.')
                        ]
                    ),
                    html.Div(
                        id='help-card',
                        children=[
                            html.H3('Barchart Visualization Help'),
                            html.P('On the left side you can choose filters for the y- and x-axis. The one option on '
                                   'top is for the y-axis, and the option beneath that is for the x-axis. You can zoom '
                                   'in, through selecting the button "zoom" and dragging with your mouse over the area '
                                   'that you want to zoom in. You can also zoom in through clicking on the button'
                                   ' "zoom in" and zoom out through clicking on the button "zoom out". Autoscale '
                                   'returns the image to its original start position. You can hover over the bars to'
                                   ' get more exact information about the bar. E.g. weather type x has y total deaths.'
                                   ' At times a known error with the rendering engine can occur: if you zoom in and the '
                                   'text of the x-axis overlaps with the label of the x-axis. To solve this simply pan '
                                   'somewhere on the chart.')
                        ]
                    ),
                    html.Div(
                        id='help-card',
                        children=[
                            html.H3('Heatmap Visualization Help'),
                            html.P(
                                'To choose your own year range move the ends of the slider. '
                                'The default is 1999-2020. To choose your own coloring factor' 
                                'click on the dropdown menu. The default factor is count of accidents. '
                                'To get more info about individual cell, place your mouse on top of it'
                                'and year, weeknumber and factor values will appear.'
                                )
                        ]
                    ),
                    html.Div(
                        id='help-card',
                        children=[
                            html.H3('Stacked Area Visualization Help'),
                            html.P('You can hover over each individual area on the chart to get more information. '
                                   'If you want to look at only particular categories e.g. for weather conditions'
                                   ' only look at “fine with high winds” you can click to disable all other categories '
                                   'and only view the one you want. \n Hovering over the filter stacked area chart icon '
                                   'brings up the controls for this visualization. Here you can change what attribute '
                                   'the color is encoding. \n You can also click and drag to look at particular areas on '
                                   'the graph. \n Hovering on the top right corner brings up more controls that are all'
                                   ' quite self-explanatory. ')
                        ]
                    ),
                    html.Div(
                        id='help-card',
                        children=[
                            html.H3('Map Visualization Help'),
                            html.P('The map supports panning and zooming. The mouse wheel can be used to zoom in on the'
                                   ' map. You can hover over the individual data points to bring up more information in'
                                   ' the form of a tooltip. \n Hovering over the filter map icon brings up the controls'
                                   ' for this visualization. Here you can select which attributes are encoded as size and'
                                   ' color. Moreover, you can select a custom year range. However if performance'
                                   ' capabilities are exceeded you will be notified to change your selection. '
                                   'The map visualization calculates a safe subset to visualize from the global '
                                   'year range. So watch out! The map does not show exactly what the global year '
                                   'range selects! If you need the years exactly use the map’s year range.')
                        ]
                    ),

                ]
            ),
        ]
    )

# Quick test to see if control panel can send data to vis boxes (answer: yes they can)
# Looks like each vis box will need its own callback function
# @app.callback(
#     Output("vis1", "children"),
#     Input("range-slider-1", "value")
# )
# def update_out_div(input_value):
#     return "Vis1: {}".format(input_value)