from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
from data_prep import get_data
import dash
import plotly.graph_objects as go
app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

with open('geojson_counties.json') as json_file:
    counties = json.load(json_file)

data = get_data()


cols_dd=["male","female","population/2010","life-expectancy"]
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[{'label': k, 'value': k} for k in cols_dd],
        value=cols_dd[0]
    ),
    dcc.Graph(
        id='display-selected-values',
    )
])


@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    print(value)
    fig = px.choropleth_mapbox(data, geojson=counties, locations='fips', color=value,
                           color_continuous_scale="Viridis",
                           range_color=(data[value].min(),data[value].max()),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
    fig.update_layout(title=f"<b>{value}</b>", title_x=0.5)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)