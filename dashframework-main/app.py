from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from jbi100_app.data import Data

from jbi100_app.views.layout import generate_nav_bar, generate_basic_layout, generate_new_layout

from dash import html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from datetime import date



# Get data by making a data object and getting the required dfs from it.
# TODO: uncomment data object once in production, currently comment for quicker start up
# data = Data()
# df_conditions, df_date, df_location, df_severity = data.get_dataframes()

df_date = pd.read_parquet('jbi100_app/assets/data/date.parquet', columns=['accident_year', 'date', 'day_of_week', 'time'])

# Make settings for slider, like mins and maxes
range_filter_global_settings = {
    'minYear' : df_date['accident_year'].min(),
    'maxYear' : df_date['accident_year'].max(),
}

# Make settings for date picker
date_filter_global_settings = {
    'minDate' : min(df_date['date']),
    'maxDate' : max(df_date['date'])
}

# print(df_date)

df_date_short = df_date.head(100)
# TODO: do something better with the temp table
table = html.Div(
            id='table-wrapper',
            children=
            dash_table.DataTable(
                id='table',
                # columns=[{"name": i, "id": i} for i in df_date_short.columns],
                # data=df_date_short.to_dict('records'),
                style_table={'maxHeight': '250px', 'overflowY' : 'scroll'},
                #maxHeight otherwise table doesnt respect parent div
            )
        )

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            id="main",
            children=[
                generate_nav_bar(),
                generate_new_layout(range_filter_global_settings, date_filter_global_settings, table),
                # need to add style otherwise graph doesnt respect height of parent div (bad graph)
                # generate_new_layout(dcc.Graph(id="bar-chart", style={'height': '100%'}, figure=fig))
            ]
        ),
    ],
)


# Global filter callback function
@app.callback(
    Output('table', 'columns'), # TODO: only changing current table, will need to change to other vis' i think
    Output('table', 'data'),
    Input('year-filter-global', 'value'),
    Input('time-filter-global', 'value'),
    Input('vehicles-slider-global', 'value'),
    Input('date-picker-global', 'start_date'),
    Input('date-picker-global', 'end_date'),
)
def global_filter(year_range, time_range, vehicle_no, start_date, end_date):
    print(year_range, time_range, vehicle_no, start_date, end_date)

    # incredibly slow filtering :(
    mask = (df_date['accident_year'] >= year_range[0]) & (df_date['accident_year'] <= year_range[1])
    df_filtered = df_date[mask]

    columns = [{"name": i, "id": i} for i in df_filtered.columns]
    data = df_filtered.to_dict('records')
    # return '{}, {}, {}, {}, {}'.format(year_range, time_range, vehicle_no, start_date, end_date)
    return columns, data

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')  # why debug not working :(
