from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
from data_prep import get_data
app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

with open('geojson_counties.json') as json_file:
    counties = json.load(json_file)

data=get_data()

import plotly.express as px

fig = px.choropleth_mapbox(data, geojson=counties, locations='fips', color='land_area (km^2)',
                           color_continuous_scale="Viridis",
                           range_color=(data['land_area (km^2)'].min(),data['land_area (km^2)'].max()),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
cols=["male","female"]
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)