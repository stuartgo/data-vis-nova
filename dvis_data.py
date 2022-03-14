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

#rename column
pres_states_winners.rename(columns={"party_detailed":"party"},inplace=True)



#Find the previous winner for each county
def previous_winner(row,state):
    if state:
        if row.name==len(pres_states_winners)-1:
            return None
        prev_row=pres_states_winners.iloc[row.name+1,:]
        if prev_row.state_fips==row.state_fips:
            return prev_row.party
    else:
        if row.name==len(pres_county_winners)-1:
            return None
        prev_row=pres_county_winners.iloc[row.name+1,:]
        if prev_row.county_fips==row.county_fips:
            return prev_row.party
    return None

pres_county_winners.sort_values(["county_fips","year"],ascending=[True,False],inplace=True)
pres_county_winners.reset_index(inplace=True)
pres_county_winners["prev_party"]=pres_county_winners.apply(lambda x: previous_winner(x,False) ,axis=1)


pres_states_winners.sort_values(["state_fips","year"],ascending=[True,False],inplace=True)
pres_states_winners.reset_index(inplace=True)
pres_states_winners["prev_party"]=pres_states_winners.apply(lambda x: previous_winner(x,True) ,axis=1)


def swing(row):
    if (row.party == "REPUBLICAN") and (row.prev_party == "REPUBLICAN"):
        # red if winning party was republican for two elections in a row
        return 0
    if (row.party == "REPUBLICAN") and (row.prev_party != "REPUBLICAN"):
        # red stripes if winning party changed from democrat to republican
        return 1
    if (row.party == "DEMOCRAT") and (row.prev_party == "DEMOCRAT"):
        # blue if winning party was democrat for two elections in a row
        return 0
    if (row.party == "DEMOCRAT") and (row.prev_party != "DEMOCRAT"):
        # red stripes if winning party changed from republican to democrat
        return 1 
    if (row.party != "DEMOCRAT") and (row.prev_party != "REPUBLICAN"):
        # choose another color for non-dem/rep parties (there's only one other)
        return 2

pres_county_winners["swing"]=pres_county_winners.apply(lambda x: swing(x),axis=1)
pres_states_winners["swing"]=pres_states_winners.apply(lambda x: swing(x),axis=1)


#geojson is required when working with counties as its not built in
with open('geojson_counties.json') as json_file:
    counties = json.load(json_file)