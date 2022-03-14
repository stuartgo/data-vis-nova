# POLITICAL LANDSCAPE OF THE USA IN THE 21ST CENTURY

#### Import libraries/modules/data ####
from lib2to3.pygram import pattern_symbols
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import json
import dash_daq as daq
from dvis_data import pres_states, pres_states_winners, pres_counties, counties, pres_county_winners
########

# App layout
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Political Landscape of the USA in the 21st Century",
        style = {"text-align": "center"}
    ),
    dcc.Slider(
        min = 2000, max = 2020, step = 4, value = 2020, # min, max, step, default of the slider
        id = "year_slider", # unique id of the slider object
        marks = {
            2000: {"label": "2000", "style": {"color": "red"}},
            2004: {"label": "2004", "style": {"color": "red"}},
            2008: {"label": "2008", "style": {"color": "blue"}},
            2012: {"label": "2012", "style": {"color": "blue"}},
            2016: {"label": "2016", "style": {"color": "red"}},
            2020: {"label": "2020", "style": {"color": "blue"}}
        },
        # vertical = 1 # uncomment to change slider to vertical orientation
    ),
    daq.ToggleSwitch(
        id='state_county_toggle',
        value=True,
        label='State?',
        labelPosition='bottom'
    ),
    # html.Div(id = 'slider_output_container'),
    html.Br(),

    dcc.Graph(id = "usa_map")
])



@app.callback(
    Output(component_id = "usa_map", component_property = "figure"),
    Input(component_id = "year_slider", component_property = "value"),
    Input(component_id = "state_county_toggle", component_property = "value")
)


def update_graph(year, state):
    # container = f"Results for the {value} elections"

    # filtering election data for current year
    pres_states_winners_copy = pres_states_winners.copy()
    pres_states_winners_copy = pres_states_winners_copy[pres_states_winners_copy.year == year]

    pres_county_winners_copy = pres_county_winners.copy()
    pres_county_winners_copy = pres_county_winners_copy[pres_county_winners_copy.year == year]

    # choropleth
    if state:
        fig = px.choropleth(
            data_frame = pres_states_winners_copy,
            locationmode = "USA-states",
            locations = "state_po",
            scope = "usa",
            color = "party",
            color_discrete_map = {"REPUBLICAN": "red", "DEMOCRAT": "blue", "DEMOCRATIC-FARMER-LABOR": "green"},
            hover_data = ["state"],
            template = "plotly_dark"
        )
        fig.add_scattergeo(
            locationmode = "USA-states",
            locations = pres_states_winners_copy["state_po"],
            text = pres_states_winners_copy["state_po"],
            featureidkey = "properties.NAME_3",
            mode = "text",
            textfont = dict(family = "arial", size = 10)
        )
        
    else:
        fig = px.choropleth(
            data_frame = pres_county_winners_copy,
            geojson = counties,
            locations = "county_fips",
            color = "party",
            color_discrete_map = {"REPUBLICAN": "red", "DEMOCRAT": "blue", "DEMOCRATIC-FARMER-LABOR": "green"},
            scope = "usa",
            hover_data = ["county_name","candidate"],
            template = "plotly_dark"
        )
        fig.update_traces(marker_line_width = 0, marker_opacity = 0.8)
        fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_geos(showsubunits = True, subunitcolor = "darkgray")
    return fig


if __name__ == "__main__":
    app.run_server(debug = True)