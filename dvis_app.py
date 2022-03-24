# POLITICAL LANDSCAPE OF THE USA IN THE 21ST CENTURY

#### Import libraries/modules/data ####
from itertools import dropwhile
from lib2to3.pygram import pattern_symbols
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import json
import dash_daq as daq
from dvis_data import pres_states, pres_states_winners, pres_counties, counties, pres_county_winners, usa_states
from skimage import io
########

# App layout
app = dash.Dash(__name__)
background_color="#1f2630"
box_color="#252e3f"
font_color="#7fafdf"
red, blue, green,grey = "#ef553b", "#636efa", "#66CC00","#f0f0f0"
graph=dcc.Loading(
    id="loading-1",
    children=[dcc.Graph(id = "usa_map",figure={"layout":{"plot_bgcolor":background_color}})],
    type="circle"
)
graph2=dcc.Loading(
    id="loading-2",
    children=[dcc.Graph(id = "graph2")],
    type="circle"
)

store=dcc.Store(id='session', storage_type='session')
slider=dcc.Slider(
                            min = 2000, max = 2020, step = 4, value = 2000, # min, max, step, default of the slider
                            id = "year_slider", # unique id of the slider object
                            marks = {
                                2000: {"label": "2000", "style": {"color": red,"font:family":"playfair display,sans-serif","font-size":"14px"}},
                                2004: {"label": "2004", "style": {"color": red,"font:family":"playfair display,sans-serif","font-size":"14px"}},
                                2008: {"label": "2008", "style": {"color": blue,"font:family":"playfair display,sans-serif","font-size":"14px"}},
                                2012: {"label": "2012", "style": {"color": blue,"font:family":"playfair display,sans-serif","font-size":"14px"}},
                                2016: {"label": "2016", "style": {"color": red,"font:family":"playfair display,sans-serif","font-size":"14px"}},
                                2020: {"label": "2020", "style": {"color": blue,"font:family":"playfair display,sans-serif","font-size":"14px"}}
                            },
                            
                            # vertical = 1 # uncomment to change slider to vertical orientation
                        )
#TODO: These bad boys need better names
name_graph1="Number of votes by party by year"
name_graph2="Number of votes by party"
name_graph3="NNNNNNEEEEEEEEh"
dropdown=dcc.Dropdown([name_graph1, name_graph2, name_graph3], name_graph1,id="dropdown", searchable=False)
app.layout = html.Div([
            store,
            html.Div([
                html.H1(
                        "Political Landscape of the USA in the 21st Century",
                        style = {"text-align": "left","font:family":"playfair display,sans-serif","color":font_color,"margin":0,"padding-top":"20px","padding-left":"20px"}
                        ),
                html.P("Interactive web application to explore the results of the presidential elections in the 21st century",
                style = {"text-align": "left","font:family":"playfair display,sans-serif","color":font_color,"padding":"20px"})
            ],style={}),
            html.Div([
                html.Div([
                        html.Div([slider],style={"background-color":box_color,"padding-top":"40px","margin-bottom":"20px"}),
                        graph,
                ],style={"width":"60%","padding-right":"20px"}),
                html.Div([
                    html.Div([dropdown],style={"margin":"20px"}),
                    graph2
                ],style={"width":"40%","background-color":box_color})
                
            ],style={"display":"flex","flex-align":"row"}),
            html.Br(),
        ],style={"background-color":background_color,"max-width":"100vw","max-height":"100vh","margin":0})
@app.callback(
    Output("session","data"),
    Input(component_id = "usa_map", component_property = "clickData"),
    State("session","data")
)
def on_click(clickdata,data):
    data=data or {"states": ["WA"]}
    if not clickdata:
        return data
    new_state=clickdata["points"][0]["location"]
    if new_state in data["states"]:
        data["states"].remove(new_state)
    else:
        data["states"].append(new_state)
    print(data,"yeet")
    return data

@app.callback(
    Output(component_id = "graph2", component_property = "figure"),
    Input(component_id = "year_slider", component_property = "value"),
    Input(component_id = "dropdown", component_property = "value"),
    Input("session","data")
)
def update_graph2(year,dropdown,data):
    print(dropdown)
    pres_states_copy = pres_states[pres_states["state_po"].isin(data["states"])].copy()
    pres_states_winners_copy = pres_states_winners.copy() 
    pres_states_winners_copy.party=pres_states_winners_copy.apply(lambda x: x.party if x.state_po in data["states"] else "None", axis=1)
    pres_states_winners_copy_year=pres_states_winners_copy.copy()
    pres_states_winners_copy = pres_states_winners_copy[pres_states_winners_copy.year == year]

    pres_states_winners_copy_year=pres_states_winners_copy_year[pres_states_winners_copy_year["state_po"].isin(data["states"])].copy()

    if dropdown==name_graph1:
        fig_2 = px.line(
            pres_states_winners_copy_year.groupby(["party","year"]).sum().reset_index(level=[0,1]),
            x="year",
            y="totalvotes",
            color="party",
            labels = {
            "totalvotes": "Number of votes",
            "year": "Year"
            },
            color_discrete_map = {
            "REPUBLICAN": red,
            "DEMOCRAT": blue,
            "OTHER": green
            }
            )
    elif dropdown==name_graph2:
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
        orientation = "v"
        )
    elif dropdown==name_graph3:
        img = io.imread('https://www.frontlinegaming.org/wp-content/uploads/2020/11/s-l500.jpg')
        fig_2 = px.imshow(img)
    fig_2.update_layout(
        # xaxis = {"categoryorder": "total descending"},
        showlegend = False,
        paper_bgcolor=box_color,
        plot_bgcolor=box_color,
        font_color=font_color
    )
    return fig_2







@app.callback(
    Output(component_id = "usa_map", component_property = "figure"),
    Input(component_id = "year_slider", component_property = "value"),
    Input("session","data")
)
def update_graph(year,data):
    # create copies of election data and filter election data for current year
    pres_states_copy = pres_states[pres_states["state_po"].isin(data["states"])].copy()
    pres_states_winners_copy = pres_states_winners.copy() #[pres_states_winners["state_po"].isin(data["states"])].copy()
    pres_states_winners_copy.party=pres_states_winners_copy.apply(lambda x: x.party if x.state_po in data["states"] else "None", axis=1)
    pres_states_winners_copy = pres_states_winners_copy[pres_states_winners_copy.year == year]

    # define colors for the parties
    
    fig_1 = px.choropleth(
        data_frame = pres_states_winners_copy,
        locationmode = "USA-states",
        locations = "state_po",
        scope = "usa",
        color = "party",
        color_discrete_map = {
            "REPUBLICAN": red,
            "DEMOCRAT": blue,
            "DEMOCRATIC-FARMER-LABOR": green,
            "None":grey
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
        textfont = dict(family = "arial", size = 10),
        hoverinfo="skip",
        showlegend=False
    )
    fig_1.update_layout(
        margin = dict(l = 0, r = 0, b = 0, t = 0, pad = 4, autoexpand = True ),
        paper_bgcolor=box_color,
        geo=dict(bgcolor=box_color),
        legend_font_color=font_color,
        legend_title="Parties"
        )

    return fig_1


if __name__ == "__main__":
    app.run_server(debug = True)