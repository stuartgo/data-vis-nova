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
from dvis_data import pres_states, pres_states_winners, pres_counties, counties, pres_county_winners, usa_states
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
    html.Button(
        "Select/Unselect All",
        id = "all_or_none_button",
        n_clicks = 0
    ),
    dcc.Checklist(
        id = "state_checklist",
        options = usa_states,
        value = ["WASHINGTON"],
    ),
    daq.ToggleSwitch(
        id='state_county_toggle',
        value=True,
        label='State?',
        labelPosition='bottom'
    ),    
    # html.Div(id = 'slider_output_container'),
    html.Br(),

    dcc.Graph(id = "usa_map"),
    dcc.Graph(id = "barplot_votes")
])


@app.callback(
    Output(component_id = "usa_map", component_property = "figure"),
    Output(component_id = "barplot_votes", component_property = "figure"),
    Input(component_id = "year_slider", component_property = "value"),
    Input(component_id = "state_checklist", component_property = "value"),
    Input(component_id = "all_or_none_button",  component_property = "value"),
    Input(component_id = "state_county_toggle", component_property = "value")
)
def update_graph(year, states_selected, n_clicks, state_toggle):
    # create copies of election data and filter election data for current year
    pres_states_copy = pres_states[pres_states["state"].isin(states_selected)].copy()
    pres_states_winners_copy = pres_states_winners[pres_states_winners["state"].isin(states_selected)].copy()
    pres_states_winners_copy = pres_states_winners_copy[pres_states_winners_copy.year == year]
    pres_county_winners_copy = pres_county_winners.copy()
    pres_county_winners_copy = pres_county_winners_copy[pres_county_winners_copy.year == year]

    # define colors for the parties
    red, blue, green = "#FF0000", "#0080FF", "#66CC00"

    # choropleth
    if state_toggle:
        fig_1 = px.choropleth(
            data_frame = pres_states_winners_copy,
            locationmode = "USA-states",
            locations = "state_po",
            scope = "usa",
            color = "party",
            color_discrete_map = {
                "REPUBLICAN": red,
                "DEMOCRAT": blue,
                "DEMOCRATIC-FARMER-LABOR": green
            },
            hover_name = "state",
            hover_data = {
                "index": False,
                "year": False,
                "state": False,
                "state_po": False,
                "state_fips": False,
                "candidate": False,
                "party": False,
                "writein": False,
                "candidatevotes": False,
                "totalvotes": True,
                "prev_party": False,
                "swing": False
            },
        )
        fig_1.add_scattergeo(
            locationmode = "USA-states",
            locations = pres_states_winners_copy["state_po"],
            text = pres_states_winners_copy["state_po"],
            featureidkey = "properties.NAME_3",
            mode = "text",
            textfont = dict(family = "arial", size = 10)
        )
        fig_1.update_layout(margin = dict(l = 0, r = 0, b = 0, t = 0, pad = 4, autoexpand = True))

        # barplot with the number of votes per party
        fig_2 = px.bar(
            data_frame = pres_states_copy[pres_states.year == year],#.sort_values("candidatevotes", ascending = False),
            x = "party",
            y = "candidatevotes",
            hover_name = "party",
            hover_data = ["candidatevotes", "state"],
            color = "party",
            color_discrete_map = {
                "REPUBLICAN": red,
                "DEMOCRAT": blue,
                "OTHER": green
            },
            labels = {
                "party": "Party",
                "candidatevotes": "Number of votes"
            },
            # title = "Number of votes per party",
            # range_y = [0, 60000000],
            category_orders = {"party": ["DEMOCRAT", "REPUBLICAN", "OTHER"]},
            width = 800,
            height = 600,
            orientation = "v"
        )
        fig_2.update_layout(
            # xaxis = {"categoryorder": "total descending"},
            showlegend = False,
        )
        
    else:
        fig_1 = px.choropleth(
            data_frame = pres_county_winners_copy,
            geojson = counties,
            locations = "county_fips",
            color = "party",
            color_discrete_map = {
                "REPUBLICAN": red,
                "DEMOCRAT": blue,
                "DEMOCRATIC-FARMER-LABOR": green
            },
            scope = "usa",
            hover_data = ["county_name","candidate"],
            # template = "plotly_dark"
        )
        fig_1.update_traces(marker_line_width = 0, marker_opacity = 0.8)
        fig_1.update_layout(margin = dict(l = 0, r = 0, b = 0, t = 0, pad = 4, autoexpand = True))
        fig_1.update_geos(showsubunits = True, subunitcolor = "black")

    return (fig_1, fig_2)


if __name__ == "__main__":
    app.run_server(debug = True)