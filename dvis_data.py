# POLITICAL LANDSCAPE OF THE USA IN THE 21ST CENTURY
# data loading and cleaning

#### Import libraries/modules ####
import pandas as pd
import numpy as np
import json
########

def load_data():
    """
    Load all of the required
    datasets, including state- and county-wide
    presidential election results, senate results,
    and information about each individual county in
    the USA.
    """

    pres_states = pd.read_csv("/data/US_President.csv") # state-level presidential elections
    senate = pd.read_csv("/data/US_Senate.csv", encoding = 'latin1') # senate elections
    electoral_college = pd.read_csv("/data/Electoral_College.csv") # electoral college votes per state
    census_2020 = pd.read_excel("/data/Census_2020.xlsx")
    pres_bios = pd.read_excel("/data/President_Info.xlsx") # information on party candidates since 2000
    pres_bios.party = pres_bios.party.str.upper()

    # drop unecessary columns
    pres_states.drop(
        columns = ["office", "version", "notes", "state_cen", "state_ic", "party_detailed"],
        inplace = True
    )
    senate.drop(
        columns = ["state_cen", "state_ic", "district", "mode", "version", "party_detailed"],
        inplace = True
    )
    electoral_college.drop(
        columns = ["Unnamed: 4"],
        inplace = True
    )

    return (pres_states, senate, electoral_college, census_2020, pres_bios)

# Import data, drop unecessary columns and rows
pres_states, senate, electoral_college, census_2020, pres_bios = load_data()
pres_states = pres_states[pres_states.year >= 1976]

# replace republican with 1 and democrat with 0
census_2020["party_2020"] = census_2020["party_2020"].replace({"REPUBLICAN": 0, "DEMOCRAT": 1})

# Rename colum and rename the libertarian party as other
pres_states.rename(columns = {"party_simplified": "party"}, inplace = True)
pres_states.party.replace({"LIBERTARIAN": "OTHER"}, inplace = True)
# Create dataframe, pres_states_winners, with most voted candidate per state per year
pres_states_winners = pres_states.copy()
pres_states_winners.sort_values(["year", "state_fips", "candidatevotes"],ascending=False,inplace=True)
pres_states_winners.drop_duplicates(["state_fips", "year"],inplace=True)


senate.rename(columns = {"party_simplified": "party"}, inplace = True)
senate=senate[senate.stage=="gen"]
senate.party.replace({"LIBERTARIAN": "OTHER"}, inplace = True)
senate_winners=senate.copy()
senate_winners.reset_index(inplace=True)
senate_winners.sort_values(["state_po","year","candidatevotes"],inplace=True,ascending=False)

senate_seats=senate_winners.groupby(["state_po","year"]).head(2)
senate_seats.reset_index(inplace=True)

senate_seats=senate_seats.groupby(['state_po','year']).agg({'party': ' '.join}).reset_index(level=[0,1])

senate_winners=senate_winners.merge(senate_seats,left_on=["year","state_po"],right_on=["year","state_po"])
senate_winners.rename(columns={"party_x":"party","party_y":"seats"},inplace=True)
print(":.....................................")
print(senate_winners)


# Create dataframe, pres_county_winners, with most voted candidate per state per year


# Find the previous winner for each county
# def previous_winner(row,state):
#     if state:
#         if row.name==len(pres_states_winners)-1:
#             return None
#         prev_row=pres_states_winners.iloc[row.name+1,:]
#         if prev_row.state_fips==row.state_fips:
#             return prev_row.party
#     else:
#         if row.name==len(pres_county_winners)-1:
#             return None
#         prev_row=pres_county_winners.iloc[row.name+1,:]
#         if prev_row.county_fips==row.county_fips:
#             return prev_row.party
#     return None


pres_states_winners.sort_values(["state_fips","year"],ascending=[True,False],inplace=True)
pres_states_winners.reset_index(inplace=True)
# pres_states_winners["prev_party"]=pres_states_winners.apply(lambda x: previous_winner(x,True) ,axis=1)

# Determine swing states
# def swing(row):
#     if (row.party == "REPUBLICAN") and (row.prev_party == "REPUBLICAN"):
#         # red if winning party was republican for two elections in a row
#         return 0
#     if (row.party == "REPUBLICAN") and (row.prev_party != "REPUBLICAN"):
#         # red stripes if winning party changed from democrat to republican
#         return 1
#     if (row.party == "DEMOCRAT") and (row.prev_party == "DEMOCRAT"):
#         # blue if winning party was democrat for two elections in a row
#         return 0
#     if (row.party == "DEMOCRAT") and (row.prev_party != "DEMOCRAT"):
#         # red stripes if winning party changed from republican to democrat
#         return 1 
#     if (row.party != "DEMOCRAT") and (row.prev_party != "REPUBLICAN"):
#         # choose another color for non-dem/rep parties (there's only one other)
#         return 2

# pres_states_winners["swing"]=pres_states_winners.apply(lambda x: swing(x),axis=1)

# list of USA states
usa_states = [
    "ALABAMA", "ALASKA", "ARIZONA","ARKANSAS", "CALIFORNIA", "COLORADO",
    "CONNECTICUT", "DELAWARE", "DISTRICT OF COLUMBIA", "FLORIDA", "GEORGIA",
    "HAWAII", "IDAHO", "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY",
    "LOUISIANA", "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN",
    "MINNESOTA", "MISSISSIPPI", "MISSOURI", "MONTANA", "NEBRASKA",
    "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY", "NEW MEXICO", "NEW WORK",
    "NORTH CAROLINA", "NORTH DAKOTA", "OHIO", "OKLAHOMA", "OREGON",
    "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA", "SOUTH DAKOTA",
    "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA", "WASHINGTON",
    "WEST VIRGINIA", "WISCONSIN", "WYOMING"
]

#geojson is required when working with counties as its not built in
# with open('geojson_counties.json') as json_file:
#     counties = json.load(json_file)


## Preprocess Electoral College dataframe
# map state to state_po
state_po_df = pres_states.drop_duplicates("state")[["state", "state_po"]]
state_po_map = {}

for key, value in zip(state_po_df.state, state_po_df.state_po):
    state_po_map[key.title()] = value

electoral_college["state_po"] = electoral_college.State.map(state_po_map)

# map Party to full party name
college_party_map = {"R": "REPUBLICAN", "D": "DEMOCRAT"}
electoral_college["Party"] = electoral_college.Party.map(college_party_map)

senate_winners["seats_labels"]=senate_winners.seats.map({"REPUBLICAN DEMOCRAT":"One each",
                                "DEMOCRAT REPUBLICAN":"One each",
                                "REPUBLICAN REPUBLICAN":"Republican",
                                "DEMOCRAT DEMOCRAT":"Democrat",
                                "DEMOCRAT OTHER":"One democrat one other",
                                "OTHER DEMOCRAT":"One democrat one other",
                                "REPUBLICAN OTHER":"One republican one other",
                                "OTHER REPUBLICAN":"One republican one other",
                                "OTHER OTHER": "Other"
                                })
