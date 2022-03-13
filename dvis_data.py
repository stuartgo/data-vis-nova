# POLITICAL LANDSCAPE OF THE USA IN THE 21ST CENTURY
# data loading and cleaning

#### Import libraries/modules ####
import pandas as pd
########

def load_data():
    """
    Load all of the required
    datasets, including state- and county-wide
    presidential election results, senate results,
    and information about each individual county in
    the USA.
    """

    pres_states = pd.read_csv("1976-2020-president.csv") # state-level presidential elections
    pres_counties = pd.read_csv("countypres_2000-2020.csv") # county-level presidential elections
    senate = pd.read_csv("1976-2020-senate.csv", encoding = 'latin1') # senate elections
    info_counties = pd.read_csv("counties.csv") # county-level information, includes coordinates

    pres_states.drop(
        columns = ["office", "version", "notes", "state_cen", "state_ic", "party_simplified"],
        inplace = True
    )
    pres_counties.drop(
        columns = ["office", "version"],
        inplace = True
    )
    senate.drop(
        columns = ["state_cen", "state_ic", "district", "mode", "version", "party_simplified"],
        inplace = True
    )

    return (pres_states, pres_counties, senate, info_counties)

# Import data, drop unecessary columns and rows
pres_states, pres_counties, senate, info_counties = load_data()
pres_states = pres_states[pres_states.year >= 1996]

# Create dataframe, pres_states_winners, with most voted candidate per state per year
pres_states_winners = pd.DataFrame()
pres_states_grouped = pres_states.groupby(["year", "state"]).max("candidatevotes")
for vote in pres_states_grouped.candidatevotes:
    pres_states_winners = pres_states_winners.append(pres_states.query("candidatevotes == @vote"))
pres_states_winners.reset_index(inplace = True, drop = True)

# Add color code to pres_states_winners dataframe based on winning party
color_code = []
for index, year, party in zip(pres_states_winners.index, pres_states_winners.year, pres_states_winners.party_detailed):
    # 51 states: subtracting 51 to current index retrieves winning party on that same state for the previous election
    if year >= 2000: # prevents index out of range error for 1996 (there's no 1992 data)
        prev_party = pres_states_winners.loc[index-51, "party_detailed"]
        if (party == "REPUBLICAN") and (prev_party == "REPUBLICAN"):
            # red if winning party was republican for two elections in a row
            color_code.append("red")
        if (party == "REPUBLICAN") and (prev_party != "REPUBLICAN"):
            # red stripes if winning party changed from democrat to republican
            color_code.append("red_stripes")
        if (party == "DEMOCRAT") and (prev_party == "DEMOCRAT"):
            # blue if winning party was democrat for two elections in a row
            color_code.append("blue")
        if (party == "DEMOCRAT") and (prev_party != "DEMOCRAT"):
            # red stripes if winning party changed from republican to democrat
            color_code.append("blue_stripes")      
        if (party != "DEMOCRAT") and (party != "REPUBLICAN"):
            # choose another color for non-dem/rep parties (there's only one other)
            color_code.append("other")
pres_states_winners = pres_states_winners[pres_states_winners.year >= 2000]
pres_states_winners["color"] = color_code