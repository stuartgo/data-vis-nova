# POLITICAL LANDSCAPE OF THE USA

#### Import libraries/modules/data ####
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_daq as daq
from dvis_data import pres_states, pres_states_winners, senate_winners, senate, electoral_college, census_2020, pres_bios
from senateGraph import senate_graph
########

# App layout

app = dash.Dash(__name__)
server = app.server
# commonly used colors
background_color = "#1f2630"
box_color = "#252e3f"
font_color = "#7fafdf"
red, blue, white, grey, purple = "#ef553b", "#636efa", "#E5E1D4","#f0f0f0","#A9629B"

# load graphs
graph = dcc.Loading(
    id = "loading-1",
    children = [dcc.Graph(id = "usa_map", figure = {"layout": {"plot_bgcolor": background_color}})],
    type = "circle"
)
graph2 = dcc.Loading(
    id = "loading-2",
    children = [dcc.Graph(id = "graph2", figure = {"layout": {"plot_bgcolor": background_color}})],
    type = "circle"
)
stacked_bars = dcc.Loading(
    id = "loading-3a",
    children = [dcc.Graph(id = "stacked_bars", figure = {"layout": go.Layout(margin = {"t": 0})})]
)
line_plot = dcc.Loading(
    id = "loading-3b",
    children = [dcc.Graph(id = "line_plot", figure = {"layout": go.Layout(margin = {"t": 0})})]
)
correlation_heatmap = dcc.Loading(
    id = "loading-4",
    children = [dcc.Graph(id = "correlation_heatmap")]
)
radar_plot = dcc.Loading(
    id = "loading-5",
    children = [dcc.Graph(id = "radar_plot")]
)

store = dcc.Store(id = 'session', storage_type = 'session')
# create a slider to select the year for which to retrieve election data
slider = dcc.Slider(
    min = 1976, max = 2020, step = 4, value = 2020, # min, max, step, default of the slider
    id = "year_slider", # unique id of the slider object
    marks = {
        1976: {"label": "1976"},
        1980: {"label": "1980"},
        1984: {"label": "1984"},
        1988: {"label": "1988"},
        1992: {"label": "1992"},
        1996: {"label": "1996"},
        2000: {"label": "2000"},
        2004: {"label": "2004"},
        2008: {"label": "2008"},
        2012: {"label": "2012"},
        2016: {"label": "2016"},
        2020: {"label": "2020"}
    }
)
#TODO: These bad boys need better names
name_graph1 = "Number of popular votes by party" 
name_graph2 = "Number of electoral votes by party"
name_graph3 = "Senate seat distribution"

dropdown = dcc.Dropdown(
    [name_graph1, name_graph2],
    name_graph2,
    id = "dropdown",
    searchable = False
)
presidential_graphs=[name_graph1, name_graph2]
senate_graphs=[name_graph1, name_graph3]



app.layout = html.Div([
    store,
    html.Div([
        html.H1(
            "Political Landscape of the United States of America",
            id = "minge",
            style = {
                "text-align": "left",
                "font:family": "playfair display,sans-serif",
                "color": font_color,
                "margin": 0,
                "padding-top": "20px",
                "padding-left": "20px"
            }
        ),
        html.P(
            "Did you know that the Republicans won all but one state in 1984? " +
            "Or that in 2 of the last 12 elections the Democrats lost despite winning the popular vote?",
            style = {
                "text-align": "left",
                "font:family": "playfair display,sans-serif",
                "color": font_color,
                "padding-left":"20px"
            }
        ),
        html.P(
            "Explore the political results in the US from 1974 to 2020. " +
            "Select one or multiple states to dynamically update the vote count. " +
            "Use the toggle to visualize the results of senate elections.",
            style = {
                "text-align": "left",
                "font:family": "playfair display,sans-serif",
                "color": font_color,
                "padding-left":"20px"                
            }
        )
        ],
        style={}
    ),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    slider,
                    html.Div([
                        html.Div(
                            ["Senate"],
                            style = {
                                "display": "flex",
                                "justify-content": "center",
                                "align-content": "center",
                                "flex-direction": "column"
                            }
                        ),
                        daq.ToggleSwitch(id = "presidential_toggle", value = True),
                        html.Div(
                            ["Presidential"],
                            style = {
                                "display": "flex",
                                "justify-content": "center",
                                "align-content": "center",
                                "flex-direction": "column"
                            }
                        )
                    ],
                    style = {
                        "display": "flex",
                        "flex-direction": "row",
                        "color": font_color,
                        "justify-content": "center"
                    })
                ],
                style = {
                    "height": "70px",
                    "margin-bottom": "10px",
                    "background-color": box_color,
                    "padding-top": "20px"
                }),
                html.Div([
                    html.Div([
                        html.Button("Select/Unselect All", id = "select-all-states", n_clicks = 0)
                    ],
                    style = {
                        "color": font_color,
                        "background-color": box_color,
                        "padding-left": "10px",
                        "padding-top": "10px"
                    }),
                    graph,
                ],
                ),
            ],
            style={"height":"100%","background-color":box_color}
            )
        ],
        style = {
            "width": "60%",
            "padding-right": "10px"
        }),
        html.Div([
            html.Div([
                    html.Div([
                        html.H3(
                            id = "democrat-candidate",
                            style = {
                                "color": blue,
                                "font-weight": "bold",
                                "font-size": "30px",
                                "text-align": "center",
                                "margin-bottom": "3px",
                                "margin-top": "15px",
                            }
                        ),
                        html.H4(
                            id = "democrat-subtext",
                            style = {
                                "color": font_color,
                                "text-align": "center",
                                "margin-top": "0px"
                            }
                        )
                    ],
                    style = {
                        "background-color": box_color,
                        "vertical-align": "top",
                        "margin-bottom": "10px",
                        "margin-right": "10px",
                        "display": "inline-block",
                        "height": "90px",
                        "width": "50%"
                    }),
                    html.Div([
                    html.H3(
                        id = "republican-candidate",
                        style = {
                            "color": red,
                            "font-weight": "bold",
                            "font-size": "30px",
                            "text-align": "center",
                            "margin-bottom": "3px",
                            "margin-top": "15px"
                        }
                    ),
                    html.H4(
                        id = "republican-subtext",
                        style = {
                            "color": font_color,
                            "text-align": "center",
                            "margin-top": "0px"
                        }
                    )
            ],
            style = {
                "background-color": box_color,
                "vertical-align": "top",
                "margin-bottom": "10px",
                "margin-right": "4px",
                "display": "inline-block",
                "height": "90px",
                "width": "50%"
            }),
                    ],
                    style={"display":"flex","flex-direction":"row"}
                    ),
        
            html.Div([
                html.Div([
                    dropdown
                ],
                style = {"margin": "20px"}),
                html.Div([
                    graph2
                ]),
            ],
            style = {
                "background-color": box_color,
                "padding-top": "10px",
                "margin-right": "5px",
            })
        ],
        style = {
            "width": "40%",
            "background-color": background_color,
        })
    ],
    style = {
        "display": "flex",
        "flex-align": "row"
    }),

    html.Div([
        html.Div([
            html.H2(
                "Mirror, mirror on the wall... who's the bluest of them all?",
                id = "graph3-title",
                style = {
                    "text-align": "left",
                    "color": font_color,
                    "font:family": "playfair display,sans-serif",
                    "padding-left": "20px",
                    "padding-top": "10px"
                }
            ),
            html.P(
                "There have been 12 presidential elections since 1976. How often has each party won in each state? Select the states you want to highlight in the map above and the desired time range by dragging the slider below.",
                style = {
                    "text-align": "left",
                    "color": font_color,
                    "font:family": "playfair display,sans-serif",
                    "padding-left": "20px"
                }
            )
        ]),
        html.Div([
            dcc.RangeSlider(
                1976, 2020, 4,
                value = [1976, 2020],
                marks = {str(year): {"label": str(year), "style": {"color": font_color}} for year in range(1976, 2021, 4)},
                allowCross = False,
                tooltip = {
                    "placement": "left",
                    "always_visible": False
                },
                id = "range-slider",
                pushable = 2,
                persistence = True
                # vertical = True,
                # verticalHeight = 860
            )
        ],
        style = {
            "width": "98.8%",
            "padding-left":"15px",
            "margin-bottom": "10px",
            "background-color": box_color,
            # "display": "inline-block",
            "vertical-align": "top"
        }),
        html.Div([
            html.Div([
                stacked_bars
            ],
            style = {
                "background-color": box_color,
                "margin-bottom": "10px",
                "margin-right": "10px",
                "width": "59.5%",
                "display": "inline-block"
            }),
            html.Div([
                line_plot
            ],
            style = {
                "background-color": box_color,
                "display": "inline-block",
                "margin-bottom": "10px",
                "width": "39.5%"
            }),
        ],
        style = {
            "background-color": background_color,
            "width": "100%",
            "height": "100%",
            "display": "inline-block",
            "vertical-align": "top",
            # "margin-top": "20px"
        })
    ],
    style = {
        "background-color": background_color,
    }),
    html.Div([
        html.Div([
            html.H2(
                "The 2020 election: correlation between demographics and winning party",
                id = "heatmap-title",
                style = {
                    "text-align": "left",
                    "color": font_color,
                    "font:family": "playfair display,sans-serif",
                    "padding-top": "20px",
                    "padding-left": "20px"
                }
            ),
            html.P(
                "In 2020, states with a higher median household income tended to vote Democrat. On the other hand, states with a higher percentage of minors leaned towards Republican.",
                style = {
                    "text-align": "left",
                    "color": font_color,
                    "font:family": "playfair display,sans-serif",
                    "padding-left": "20px",
                    "padding-bottom": "10px"
                }
            )
        ],
        style = {
            "background-color": background_color
        }),
        html.Div([
            html.Div([
                dcc.Checklist([
                    "Ethnicity",
                    "Age bracket",
                    "Nationality",
                    "Employment",
                    "Education",
                    "Health",
                    "Wealth",
                    "Others"
                    ],
                    ["Ethnicity"],
                    id = "correlation-checklist",
                    style = {
                        "color": font_color,
                        "font-size": 18,
                        "font:family": "playfair display,sans-serif",
                        "padding-top": "15px"
                    })
            ],
            style = {
                "height": "50px",
                "text-align": "center",
                "align-content": "center",
                "margin-bottom": "10px",
                "background-color": box_color
            }),
            html.Div([
                correlation_heatmap
            ],
            style = {
                "margin-bottom": "20px",
                "background-color": box_color
            })
        ],
        style = {
            "display": "inline-block",
            "vertical-align": "top",
            "padding-right": "10px",
            # "padding-right": "20px",
            "font:family": "playfair display,sans-serif",
            "color": font_color,
            "background-color": background_color,
            "height":"100%",
            "width":"50%"
        }),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    [state for state in census_2020.state.unique()],
                    id = "state-dropdown",
                    multi = True,
                    value = ["Alabama", "Alaska"],       
                    style = {
                        "color": font_color
                    }
                )
            ],
            style = {
                "margin-left": "20px",
                "margin-top": "10px"
            }),
            html.Div([
                radar_plot
            ],
            style = {
                "margin-bottom": "20px",
                "margin-left": "20px"})
        ],
        style = {
            "vertical-align": "top",
            "display": "inline-block",
            "background-color": box_color,
            "width":"49%",
            "height":"100%"
        }),
    ],
    style = {
        "background-color": background_color,
        "margin-top": "20px"
    }),

html.Div([html.P("Stuart Ottersen m20210703"),
        html.P("Nuno Melo m20210681"),
        html.P("Ivan Parac m20210689")
        ],
style={
    "color":font_color
}),
html.Div([
    html.P("Sources"),
    html.A("Election data",href="https://electionlab.mit.edu/data"),
    html.A("Electoral college votes", href="https://www.kaggle.com/datasets/daithibhard/us-electoral-college-votes-per-state-17882020"),
    html.A("Census data",href="https://www.census.gov/data/datasets/2020/dec/2020-census-redistricting-summary-file-dataset.html")
],
style={
    "display":"flex",
    "flex-direction":"column",
    "color":font_color
}),

],
style = {
    "background-color": background_color,
    "max-width":"100%",
    "min-height": "90vh"
})

@app.callback(
    Output(component_id = "year_slider",component_property="marks"),
    Output(component_id = "year_slider",component_property="min"),
    Output(component_id = "year_slider",component_property="max"),
    Output(component_id = "year_slider",component_property="step"),
    Output(component_id="dropdown",component_property="options"),
    Output(component_id="dropdown",component_property="value"),
    Input(component_id = "presidential_toggle", component_property = "value"),
)
def presidential_toggle(presidential_toggle):
    
    if presidential_toggle:
         return {
            1976: {"label": "1976", "style": {"color": font_color}},
            1980: {"label": "1980", "style": {"color": font_color}},
            1984: {"label": "1984", "style": {"color": font_color}},
            1988: {"label": "1988", "style": {"color": font_color}},
            1992: {"label": "1992", "style": {"color": font_color}},
            1996: {"label": "1996", "style": {"color": font_color}},
            2000: {"label": "2000", "style": {"color": font_color}},
            2004: {"label": "2004", "style": {"color": font_color}},
            2008: {"label": "2008", "style": {"color": font_color}},
            2012: {"label": "2012", "style": {"color": font_color}},
            2016: {"label": "2016", "style": {"color": font_color}},
            2020: {"label": "2020", "style": {"color": font_color}}
        },1976,2020,4,presidential_graphs,name_graph1
        
    else:
        temp = {}
        for i in range(1976, 2022, 2):
            temp[i] = {"label": str(i)}
        return temp, 1976, 2020, 2,senate_graphs,name_graph1


@app.callback(
    Output(component_id = "select-all-states", component_property = "style"),
    Input(component_id = "presidential_toggle", component_property = "value"),
)
def hide_button(presidential):
    if presidential:
        return {"display":"block"}
    else:
        return {"display":"none"}




@app.callback(
    Output("session", "data"),
    Input(component_id = "usa_map", component_property = "clickData"),
    Input(component_id = "presidential_toggle", component_property = "value"),
    Input(component_id = "year_slider", component_property = "value"),
    State("session","data"),
    Input(component_id = "select-all-states", component_property = "n_clicks")
)
def on_click(clickdata, presidential, year, data,n_clicks):
    ctx = dash.callback_context
    if ctx.triggered[0]["prop_id"]=="select-all-states.n_clicks":
        if len(data["states"])==len(list(pres_states.state_po.unique())):
            data["states"]=[]
        else:
            data["states"]=list(pres_states.state_po.unique())
        return data
    #initialize or get session data
    data = data or {"states": []}
    #sets presidential boolean in session data
    data["presidential"] = presidential
    if not presidential:
        data["states"]=list(set(senate[senate.year==year].state_po.unique()))
    #when webapp starts there is no clickdata so this prevents an error
    if not clickdata:
        return data
    #gets data on which state was clicked
    new_state = clickdata["points"][0]["location"]
    #prevents state from being updated when clicking the presidential toggle
    if not ctx.triggered[0]["prop_id"]=="presidential_toggle.value":
        #update the visbility of a state
        if new_state in data["states"]:
            data["states"].remove(new_state)
        else:
            data["states"].append(new_state)
    #removes states from secondary graph that are not part of the senate elections
    return data


@app.callback(
    Output(component_id = "democrat-candidate", component_property = "children"),
    Output(component_id = "democrat-subtext", component_property = "children"),
    Output(component_id = "republican-candidate", component_property = "children"),
    Output(component_id = "republican-subtext", component_property = "children"),
    Output(component_id = "democrat-candidate", component_property = "style"),
    Output(component_id = "republican-candidate", component_property = "style"),
    Input(component_id = "year_slider", component_property = "value")
)
def presidential_candidates(year):
    if year not in (range(1976, 2021, 4)):
        dem_subtext = f"No presidential election in {year}"
        rep_subtext = f"No presidential election {year}"

        return ("", dem_subtext, "", rep_subtext, {}, {})

    else:
        pres_bios_copy = pres_bios[pres_bios.year == year].copy()
        dem_candidate = pres_bios_copy.loc[(pres_bios_copy.party == "DEMOCRAT"), "candidate"]
        rep_candidate = pres_bios_copy.loc[(pres_bios_copy.party == "REPUBLICAN"), "candidate"]
        dem_electoral_votes = pres_bios_copy.loc[(pres_bios_copy.party == "DEMOCRAT"), "electoral_vote"].values.tolist()[0]
        rep_electoral_votes = pres_bios_copy.loc[(pres_bios_copy.party == "REPUBLICAN"), "electoral_vote"].values.tolist()[0]
        dem_pop_vote = pres_bios_copy.loc[(pres_bios_copy.party == "DEMOCRAT"), "pop_vote_pc"].values.tolist()[0]
        rep_pop_vote = pres_bios_copy.loc[(pres_bios_copy.party == "REPUBLICAN"), "pop_vote_pc"].values.tolist()[0]

        # prevents empty black boxes when there was no presidential election in the selected year (senate view)
        dem_subtext = f"Pop. vote: {dem_pop_vote}% | Electoral votes: {dem_electoral_votes}"
        rep_subtext = f"Pop. vote: {rep_pop_vote}% | Electoral votes: {rep_electoral_votes}"
        if pres_bios_copy.loc[pres_bios_copy.party == "DEMOCRAT", "winner"].tolist()[0] == True:
            dem_style = {
                "color": blue,
                "font-weight": "bold",
                "font-size": "30px",
                "text-align": "center",
                "margin-bottom": "3px",
                "margin-top": "15px",
                "text-decoration": "underline"
            }
            rep_style = {
                "color": red,
                "font-weight": "bold",
                "font-size": "30px",
                "text-align": "center",
                "margin-bottom": "3px",
                "margin-top": "15px"
            }
        else:
            dem_style = {
                "color": blue,
                "font-weight": "bold",
                "font-size": "30px",
                "text-align": "center",
                "margin-bottom": "3px",
                "margin-top": "15px",
            }
            rep_style = {
                "color": red,
                "font-weight": "bold",
                "font-size": "30px",
                "text-align": "center",
                "margin-bottom": "3px",
                "margin-top": "15px",
                "text-decoration": "underline"
            }
        return (dem_candidate, dem_subtext, rep_candidate, rep_subtext, dem_style, rep_style)


# radar plot of two specified states
@app.callback(
    Output(component_id = "radar_plot", component_property = "figure"),
    Input(component_id = "state-dropdown", component_property = "value"),
    Input(component_id = "correlation-checklist", component_property = "value")
)
def update_radar_plot(state_dropdown, checklist):
    cols_dictionary = {
        "Ethnicity": ["White", "Indian", "Black", "Asian"],
        "Age bracket": ["Under 18", "18 to 65", "Over 65"],
        "Nationality": ["Foreign born", "Don't speak english at home"],
        "Employment": ["Unemployed", "Private sector", "Public sector", "Self-employed"],
        "Education": ["Highschool or higher", "BSc or higher"],
        "Health": ["Disabled", "No health insurance"],
        "Wealth": ["Median gross rent", "Median household income", "Poverty"],
        "Others": ["Households with computer", "Households with internet", "Mean commute time"]
    }

    cols_selected = []
    for check in checklist:
        cols = cols_dictionary[check]
        cols_selected += cols

    radar_plot = go.Figure()
    # if statement prevents an error if no state is selected in the dropdown
    if type(state_dropdown) == list:
        for state in state_dropdown:
            radar_plot.add_trace(
                go.Scatterpolar(
                    r = [item for sublist in census_2020.loc[census_2020.state == state, cols_selected].copy().values.tolist() for item in sublist],
                    theta = [column for column in census_2020.loc[census_2020.state == state, cols_selected]],
                    fill = "toself",
                    name = state
                )
            )
    radar_plot.update_layout(
        margin = dict(l= 20, r = 10, t = 25, b = 20),
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        font = dict(
            size = 12,
            color = font_color
        )
    )

    # parallel_coords = px.parallel_coordinates(
    #     census_2020,
    #     color = "party_2020",
    #     color_continuous_scale = "Bluered_r",
    #     color_continuous_midpoint = 0.5,
    #     dimensions = cols_selected
    # )

    # parallel_coords.update_layout(
    #     paper_bgcolor = "rgba(0,0,0,0)",
    #     # plot_bgcolor = 'rgba(255,255,255,0.8)',
    #     font = dict(
    #         size = 14,
    #         color = "black"
    #     )
    #     )

    return radar_plot

@app.callback(
    Output(component_id = "correlation_heatmap", component_property = "figure"),
    Input(component_id = "correlation-checklist", component_property = "value")
)
def update_correlation_heatmap(checklist):
    cols_dictionary = {
        "Ethnicity": ["White", "Indian", "Black", "Asian"],
        "Age bracket": ["Under 18", "18 to 65", "Over 65"],
        "Nationality": ["Foreign born", "Don't speak english at home"],
        "Employment": ["Unemployed", "Private sector", "Public sector", "Self-employed"],
        "Education": ["Highschool or higher", "BSc or higher"],
        "Health": ["Disabled", "No health insurance"],
        "Wealth": ["Median gross rent", "Median household income", "Poverty"],
        "Others": ["Households with computer", "Households with internet", "Mean commute time"]
    }
    cols_selected = []
    for check in checklist:
        cols = cols_dictionary[check]
        cols_selected += cols

    census_2020_x = census_2020[cols_selected]

    # census_2020_x = census_2020[cols]
    census_2020_y = census_2020["party_2020"]
    democrat_pearson_corr = {}

    for col in list(census_2020_x.columns):
        democrat_pearson_corr[col] = [np.corrcoef(census_2020_x[col], census_2020_y)[0, 1]]
        
    pearson_corr = {var: corr for var, corr in sorted(democrat_pearson_corr.items(), key = lambda item: item[1])}
    pearson_corr_df = pd.DataFrame.from_dict(pearson_corr)

    fig_4 = px.imshow(
        pearson_corr_df,
        zmin = -1,
        zmax = 1,
        color_continuous_scale = "Bluered_r",
        color_continuous_midpoint = 0,
    )
    fig_4.update_layout(
        yaxis = dict(showticklabels = False),
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        font_color = font_color,
        showlegend = False,

    )

    return fig_4


@app.callback(
    Output(component_id = "stacked_bars", component_property = "figure"),
    Output(component_id = "line_plot", component_property = "figure"),
    Input(component_id = "range-slider", component_property = "value"),
    Input("session","data")
)
def update_year_range_plots(year_range, data):
    # filters dataframe according to the year range selected in the slider
    min_year, max_year = year_range[0], year_range[1]
    electoral_college_copy = electoral_college[(electoral_college.Year >= min_year) & (electoral_college.Year <= max_year)].copy()
    # DC has no associated state po so fixing that before grouping with it
    electoral_college_copy.loc[electoral_college_copy.State == "D.C.", "state_po"] = "DC"
    electoral_college_copy = electoral_college_copy.groupby(["State", "state_po" ,"Party"])["Votes"].count().reset_index()
    # if the year range selected results in a state having no democrat or republican wins, this loop will create an entry for that state with a count of 0 victories
    # if these 0-count entries are not created, bars will simply disappear from the graph
    for state, state_po in zip(electoral_college_copy.State, electoral_college_copy.state_po):
        if electoral_college_copy[electoral_college_copy.State == state].shape[0] == 1:
            party = electoral_college_copy.loc[electoral_college_copy.State == state, "Party"].values
            if party == "REPUBLICAN":
                df_concat = pd.DataFrame({
                    "State": state,
                    "state_po": state_po,
                    "Party": ["DEMOCRAT"],
                    "Votes": [0]
                })
            elif party == "DEMOCRAT":
                df_concat = pd.DataFrame({
                    "State": state,
                    "state_po": state_po,
                    "Party": ["REPUBLICAN"],
                    "Votes": [0]
                })
            electoral_college_copy = pd.concat([electoral_college_copy, df_concat], ignore_index = True, axis = 0).sort_values(["State", "Party"])
    # DC state_po gets assigned NaN, fixing that
    electoral_college_copy.loc[electoral_college_copy.State == "D.C.", "state_po"] = "DC"
    # determine number of democrat and republican votes
    dem_votes = electoral_college_copy.loc[electoral_college_copy.Party == "DEMOCRAT", :].set_index("State")[["Votes", "state_po"]].sort_values("Votes", ascending = False)
    rep_votes = electoral_college_copy.loc[electoral_college_copy.Party == "REPUBLICAN", :].set_index("State")[["Votes", "state_po"]].reindex(dem_votes.index)
    selected_states = data["states"]

    color_state = []

    for state in dem_votes["state_po"].values.tolist():
        if state in selected_states:
            color_state.append(True)
        else:
            color_state.append(False)

    def bar_color_democrat(i):
        if i:
            return blue
        else:
            return background_color

    def bar_color_republican(i):
        if i:
            return red
        else:
            return box_color
            
    stacked_bars = go.Figure()
    stacked_bars.add_bar(
        x = dem_votes.index,
        y = dem_votes["Votes"]/(dem_votes["Votes"]+rep_votes["Votes"])*100,
        marker_color = list(map(bar_color_democrat, color_state)),
        name = "Democrat",
        showlegend = False
    )
    stacked_bars.add_bar(
        x = rep_votes.index,
        y = rep_votes["Votes"]/(dem_votes["Votes"]+rep_votes["Votes"])*100,
        marker_color = list(map(bar_color_republican, color_state)),
        name = "Republican",
        showlegend = False
    )
    stacked_bars.update_layout(
        margin = dict(l = 70, r = 20, b = 150, t = 30, autoexpand = True),
        xaxis_title = "State",
        yaxis_title = "Victories, %",
        hovermode = "x",
        barmode = "stack",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font = dict(size = 12),
        font_color = font_color
    )
    stacked_bars.add_hline(
        y = 50,
        line_width = 2,
        line_dash = "dash",
        line_color = "white",
    )

    pres_states_copy = pres_states[(pres_states.year >= min_year) & (pres_states.year <= max_year)].copy()
    pres_states_copy = pres_states_copy[pres_states["state_po"].isin(data["states"])]

    line_plot = px.line(
        pres_states_copy.groupby(["year","party"]).sum().reset_index(level=[0,1]),
        x = "year",
        y = "candidatevotes",
        color = "party",
        labels = {
            "candidatevotes": "Number of popular votes",
            "year": "Year"
        },
        range_x = [min_year-1, max_year+1],
        color_discrete_map = {
            "REPUBLICAN": red,
            "DEMOCRAT": blue,
            "OTHER": white
        },
        markers = True
    )

    line_plot.update_traces(
        line = dict(width = 5),
        marker = dict(size = 12)
    )

    line_plot.update_layout(
        margin = dict(l = 100, r = 50, b = 60, t = 40),
        paper_bgcolor = box_color,
        plot_bgcolor = box_color,
        # legend = dict(yanchor = "top", y = 1.3, xanchor = "left", x = -0.1, font = dict(size = 10)),
        showlegend = False,
        font = dict(size = 12),
        font_color = font_color,
        xaxis = dict(
            tickmode = "linear",
            dtick = 4
        )
    )

    return stacked_bars, line_plot


@app.callback(
    Output(component_id = "graph2", component_property = "figure"),
    Input(component_id = "year_slider", component_property = "value"),
    Input(component_id = "dropdown", component_property = "value"),
    Input("session", "data"),
    Input(component_id = "presidential_toggle", component_property = "value")
)
def update_graph2(year, dropdown, data, presidential):
    electoral_college_copy = electoral_college[electoral_college["state_po"].isin(data["states"])].copy()

    if presidential:
        data_graph = pres_states[pres_states["state_po"].isin(data["states"])].copy()
    else:
        data_graph = senate[senate["state_po"].isin(data["states"])].copy()

    if dropdown == name_graph1:
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
                "OTHER": white
            },
            labels = {
                "party": "Party",
                "candidatevotes": "Number of popular votes"
            },
            category_orders = {"party": ["DEMOCRAT", "REPUBLICAN", "OTHER"]},
            orientation = "v",
        )
    elif dropdown == name_graph2:
        fig_2 = px.bar(
            data_frame = electoral_college_copy[electoral_college_copy.Year == year],
            x = "Party",
            y = "Votes",
            hover_name = "State",
            hover_data = ["state_po", "Votes"],
            color = "Party",
            color_discrete_map = {
                "REPUBLICAN": red,
                "DEMOCRAT": blue
            },
            labels = {
                "Party": "Party",
                "Votes": "Number of electoral college votes"
            },
            category_orders = {"Party": ["DEMOCRAT", "REPUBLICAN"]}
        )
    elif dropdown == name_graph3:
        fig_2 = senate_graph(year,senate_winners,color_map={
            "REPUBLICAN": red,
            "DEMOCRAT": blue,
            "DEMOCRATIC-FARMER-LABOR": white,
            "None":grey,
            "OTHER": white
        })
        fig_2.update_layout(
            legend_title="Parties",
            legend_font_color=font_color,
        )

    fig_2.update_layout(
        # xaxis = {"categoryorder": "total descending"},
        showlegend = False,
        paper_bgcolor = box_color,
        plot_bgcolor = box_color,
        # font_color = font_color,
        font = dict(
            size = 12,
            color = font_color
        )
    )

    return fig_2


@app.callback(
    Output(component_id = "usa_map", component_property = "figure"),
    Input(component_id = "year_slider", component_property = "value"),
    Input("session", "data"),
    Input(component_id = "presidential_toggle", component_property = "value")
)
def update_graph(year, data, presidential):
    if presidential:
        pres_states_winners_copy = pres_states_winners.copy() #[pres_states_winners["state_po"].isin(data["states"])].copy()??
        pres_states_winners_copy.party = pres_states_winners_copy.apply(lambda x: x.party if x.state_po in data["states"] else "None", axis=1)
        graph_data = pres_states_winners_copy[pres_states_winners_copy.year == year]
        color_var = "party"
        color_map={
            "REPUBLICAN": red,
            "DEMOCRAT": blue,
            "DEMOCRATIC-FARMER-LABOR": white,
            "None":grey,
            "OTHER": white
        }
    else:
        senate_winners_copy=senate_winners.copy()
        senate_winners_copy.party=senate_winners_copy.apply(lambda x: x.party if x.state_po in data["states"] else "None", axis=1)
        graph_data= senate_winners_copy[senate_winners_copy.year == year]
        graph_data.dropna(inplace=True)
        color_var="seats_labels"
        color_map={
            "Republican": red,
            "Democrat":blue,
            "One each": purple,
            "Other": white,
            "One republican one other":"#b18b20",
            "One democrat one other":"#65a270",
        }
        
    usa_choropleth = px.choropleth(
        data_frame = graph_data,
        locationmode = "USA-states",
        locations = "state_po",
        scope = "usa",
        #color = color_var,
        #color_discrete_map = color_map,
        hover_name = "state",
        hover_data = ["totalvotes"]
    )


    scatter_geo=px.scatter_geo(graph_data[graph_data.party!="None"],locations="state_po",locationmode="USA-states",size="totalvotes", color=color_var,color_discrete_map=color_map,scope="usa",size_max=60)

    
    for trace in scatter_geo.data:
        usa_choropleth.add_trace(trace)

    usa_choropleth.add_scattergeo(
        locationmode = "USA-states",
        locations = graph_data["state_po"],
        text = graph_data["state_po"],
        featureidkey = "properties.NAME_3",
        mode = "text",
        textfont = dict(family = "arial", size = 10),
        hoverinfo = "skip",
        showlegend = False,
    )

    usa_choropleth.update_layout(
        margin = dict(l = 0, r = 0, b = 0, t = 0, pad = 4, autoexpand = True),
        paper_bgcolor = box_color,
        geo = dict(
            projection = go.layout.geo.Projection(type = 'albers usa'),
            showlakes = True,
            lakecolor = box_color,
            bgcolor = box_color
        ),
        legend_font_color = font_color,
        legend_title = "Parties"
        )
    for choropleth in usa_choropleth["data"]:
        if choropleth.name == "":
            choropleth.colorscale=[[0.0, white], [1.0, white]]
            choropleth.showlegend = False

    return usa_choropleth


if __name__ == "__main__":
    app.run_server(debug = True)