# POLITICAL LANDSCAPE OF THE USA IN THE 21ST CENTURY
# data loading and cleaning

#### Import libraries/modules ####
import pandas as pd
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

    pres_states = pd.read_csv("1976-2020-president.csv") # state-level presidential elections
    pres_counties = pd.read_csv("countypres_2000-2020.csv") # county-level presidential elections
    senate = pd.read_csv("1976-2020-senate.csv", encoding = 'latin1') # senate elections
    info_counties = pd.read_csv("counties.csv") # county-level information, includes coordinates

        #fixes fips of counties
    pres_counties.dropna(inplace=True)
    pres_counties.county_fips=pres_counties.county_fips.astype(int)
    pres_counties.county_fips=pres_counties.county_fips.apply(lambda x: str("0"*int((5-len(str(x))))+str(x)) if len(str(x))<5 else str(x))


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
pres_states_winners = pres_states.copy()
pres_states_winners.sort_values(["year","state_fips","candidatevotes"],ascending=False,inplace=True)
pres_states_winners.drop_duplicates(["state_fips","year"],inplace=True)


# Create dataframe, pres_county_winners, with most voted candidate per state per year
pres_county_winners = pres_counties.copy()
pres_county_winners.sort_values(["year","county_fips","candidatevotes"],ascending=False,inplace=True)
pres_county_winners.drop_duplicates(["county_fips","year"],inplace=True)

#Find the previous winner for each county
def previous_winner(row):
    if row.name==len(pres_county_winners)-1:
        return None
    prev_row=pres_county_winners.iloc[row.name+1,:]
    if prev_row.county_fips==row.county_fips:
        return prev_row.party
    else:
        return None



pres_county_winners.sort_values(["county_fips","year"],ascending=[True,False],inplace=True)
pres_county_winners.reset_index(inplace=True)
print(pres_county_winners)
pres_county_winners["prev_winner"]=pres_county_winners.apply(lambda x: previous_winner(x) ,axis=1)

print(pres_county_winners)

# Add color code to pres_states_winners dataframe based on winning party
# color_code_state = []
# for index, year, party in zip(pres_states_winners.index, pres_states_winners.year, pres_states_winners.party_detailed):
#     # 51 states: subtracting 51 to current index retrieves winning party on that same state for the previous election
#     if year >= 2000: # prevents index out of range error for 1996 (there's no 1992 data)
#         prev_party = pres_states_winners.loc[index-51, "party_detailed"]
#         if (party == "REPUBLICAN") and (prev_party == "REPUBLICAN"):
#             # red if winning party was republican for two elections in a row
#             color_code_state.append("red")
#         if (party == "REPUBLICAN") and (prev_party != "REPUBLICAN"):
#             # red stripes if winning party changed from democrat to republican
#             color_code_state.append("red_stripes")
#         if (party == "DEMOCRAT") and (prev_party == "DEMOCRAT"):
#             # blue if winning party was democrat for two elections in a row
#             color_code_state.append("blue")
#         if (party == "DEMOCRAT") and (prev_party != "DEMOCRAT"):
#             # red stripes if winning party changed from republican to democrat
#             color_code_state.append("blue_stripes")      
#         if (party != "DEMOCRAT") and (party != "REPUBLICAN"):
#             # choose another color for non-dem/rep parties (there's only one other)
#             color_code_state.append("other")
# pres_states_winners = pres_states_winners[pres_states_winners.year >= 2000]
# pres_states_winners["color"] = color_code_state



#geojson is required when working with counties as its not built in
with open('geojson_counties.json') as json_file:
    counties = json.load(json_file)


