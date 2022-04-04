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
from dvis_data import pres_states, pres_states_winners, pres_counties, pres_county_winners, usa_states,senate_winners,senate
from skimage import io
########

# App layout

external_scripts=[{
    "src":"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js",
    "ingegrity":"sha512-894YE6QWD5I59HgZOGReFYm4dnWc1Qt5NtvYSaNcOP+u1T9qYdvdihz0PPSiiqn/+/3e7Jo4EaG7TubfWGUrMQ==",
    "crossorigin":"anonymous"
}]
app = dash.Dash(__name__,external_scripts=external_scripts)
background_color="#1f2630"
box_color="#252e3f"
font_color="#7fafdf"
red, blue, green,grey,purple = "#ef553b", "#636efa", "#66CC00","#f0f0f0","#A9629B"
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
                            marks={
                                2000: {"label": "2000", "style": {"color": red}},
                                2004: {"label": "2004", "style": {"color": red}},
                                2008: {"label": "2008", "style": {"color": blue}},
                                2012: {"label": "2012", "style": {"color": blue}},
                                2016: {"label": "2016", "style": {"color": red}},
                                2020: {"label": "2020", "style": {"color": blue}}
                            }
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
                        "Political Landscape of the USA in the 21st Century", id="minge",
                        style = {"text-align": "left","font:family":"playfair display,sans-serif","color":font_color,"margin":0,"padding-top":"20px","padding-left":"20px"}
                        ),
                html.P("Interactive web application to explore the results of the presidential elections in the 21st century",
                style = {"text-align": "left","font:family":"playfair display,sans-serif","color":font_color,"padding":"20px"})
            ],style={}),
            html.Div([
                html.Div([
                        html.Div([
                                html.Div([
                                        slider,
                                        html.Div([
                                            html.Div(["Senate"],style={"display":"flex","justify-content":"center","align-content":"center","flex-direction":"column"}),
                                            daq.ToggleSwitch( id="presidential_toggle",value=True),
                                            html.Div(["Presidential"],style={"display":"flex","justify-content":"center","align-content":"center","flex-direction":"column"})
                                        ],style={"display":"flex","flex-direction":"row","color":font_color,"justify-content":"center"})
                                    ],style={"margin-bottom":"20px","background-color":box_color,"padding-top":"20px"}),
                                graph,
                                ])
                    ],style={"width":"60%","padding-left":"20px","padding-right":"20px"}),
                html.Div([
                    html.Div([dropdown],style={"margin":"20px"}),
                    graph2
                ],style={"width":"40%","background-color":box_color,"margin-right":"20px"})
                
            ],style={"display":"flex","flex-align":"row"}),
            html.Br(),
        ],style={"background-color":background_color,"min-width":"100vw","min-height":"100vh"})



@app.callback(
    Output(component_id="year_slider",component_property="marks"),
    Output(component_id="year_slider",component_property="min"),
    Output(component_id="year_slider",component_property="max"),
    Output(component_id="year_slider",component_property="step"),
    Input(component_id = "presidential_toggle", component_property = "value"),
)
def presidential_toggle(presidential_toggle):
    if presidential_toggle:
         return {
                                2000: {"label": "2000", "style": {"color": red}},
                                2004: {"label": "2004", "style": {"color": red}},
                                2008: {"label": "2008", "style": {"color": blue}},
                                2012: {"label": "2012", "style": {"color": blue}},
                                2016: {"label": "2016", "style": {"color": red}},
                                2020: {"label": "2020", "style": {"color": blue}}
                            },2000,2020,4

        
    else:
        temp={}
        for i in range(1976,2022,2):
            temp[i]={"label":str(i)}
        return temp,1976,2020,2




@app.callback(
    Output("session","data"),
    Input(component_id = "usa_map", component_property = "clickData"),
    Input(component_id = "presidential_toggle", component_property = "value"),
    Input(component_id = "year_slider", component_property = "value"),
    State("session","data")
)
def on_click(clickdata,presidential,year,data):
    ctx = dash.callback_context
    print(clickdata)
    #initialize or get session data
    data=data or {"states": []}
    #sets presidential boolean in session data
    data["presidential"]=presidential
    #when webapp starts there is no clickdata so this prevents an error
    if not clickdata:
        return data
    #gets data on which state was clicked
    new_state=clickdata["points"][0]["location"]
    #prevents state from being updated when clicking the presidential toggle
    print(ctx.triggered)
    if not ctx.triggered[0]["prop_id"]=="presidential_toggle.value":
        #update the visbility of a state
        if new_state in data["states"]:
            data["states"].remove(new_state)
        else:
            data["states"].append(new_state)
    #removes states from secondary graph that are not part of the senate elections
    data["states"]=list(set(data["states"])- (set(senate.state_po.unique())-set(senate[senate.year==year].state_po.unique())))
    return data

@app.callback(
    Output(component_id = "graph2", component_property = "figure"),
    Input(component_id = "year_slider", component_property = "value"),
    Input(component_id = "dropdown", component_property = "value"),
    Input("session","data"),
    Input(component_id = "presidential_toggle", component_property = "value")
)
def update_graph2(year,dropdown,data,presidential):
    print(data)
    if presidential:
        data_graph = pres_states[pres_states["state_po"].isin(data["states"])].copy()
    else:
        data_graph=senate[senate["state_po"].isin(data["states"])].copy()
       
    if dropdown==name_graph1: #This graph might not make sense when it plots all the years
        fig_2 = px.line(
            data_graph.groupby(["year","party"]).sum().reset_index(level=[0,1]),
            x="year",
            y="candidatevotes",
            color="party",
            labels = {
            "candidatevotes": "Number of votes",
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
        data_frame = data_graph[data_graph.year == year],#.sort_values("candidatevotes", ascending = False),
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
    Input("session","data"),
    Input(component_id = "presidential_toggle", component_property = "value")
)
def update_graph(year,data,presidential):
    # create copies of election data and filter election data for current year
    #pres_states_copy = pres_states[pres_states["state_po"].isin(data["states"])].copy()
    if presidential:
        pres_states_winners_copy = pres_states_winners.copy() #[pres_states_winners["state_po"].isin(data["states"])].copy()
        pres_states_winners_copy.party=pres_states_winners_copy.apply(lambda x: x.party if x.state_po in data["states"] else "None", axis=1)
        graph_data= pres_states_winners_copy[pres_states_winners_copy.year == year]
        color_var="party"
        color_map={
            "REPUBLICAN": red,
            "DEMOCRAT": blue,
            "DEMOCRATIC-FARMER-LABOR": green,
            "None":grey,
            "OTHER":green
        }
    else:
        senate_winners_copy=senate_winners.copy()
        senate_winners_copy.party=senate_winners_copy.apply(lambda x: x.party if x.state_po in data["states"] else "None", axis=1)
        graph_data= senate_winners_copy[senate_winners_copy.year == year]
        color_var="seats"
        color_map={
            "REPUBLICAN REPUBLICAN": red,
            "DEMOCRAT DEMOCRAT":blue,
            "DEMOCRAT REPUBLICAN": purple,
            "REPUBLICAN DEMOCRAT":purple,
            "OTHER OTHER": green
        }
        
        
    # define colors for the parties
    
    fig_1 = px.choropleth(
        data_frame = graph_data,
        locationmode = "USA-states",
        locations = "state_po",
        scope = "usa",
        color = color_var,
        color_discrete_map = color_map,
        hover_name = "state",
        hover_data = ["totalvotes"]
        # {
        #     "index": False,
        #     "year": False,
        #     "state": False,
        #     "state_po": False,
        #     "state_fips": False,
        #     "candidate": False,
        #     "party": False,
        #     "writein": False,
        #     "candidatevotes": False,
        #     "totalvotes": True,
        #     "prev_party": False,
        #     "swing": False
        # },
    )
    fig_1.add_scattergeo(
        locationmode = "USA-states",
        locations = graph_data["state_po"],
        text = graph_data["state_po"],
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
    for choropleth in fig_1["data"]:
        if choropleth.name=="None":
            choropleth.showlegend=False
    return fig_1


if __name__ == "__main__":
    app.run_server(debug = True)