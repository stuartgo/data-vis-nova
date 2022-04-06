
import plotly.express as px
import pandas as pd
from dvis_data import pres_counties
import json
print(pres_counties)
data=pres_counties[pres_counties.party.isin(["DEMOCRAT"])].groupby(["year","county_fips","party"]).sum().reset_index(level=[0,1]).sort_values("county_fips")
data_rep=pres_counties[pres_counties.party.isin(["REPUBLICAN"])].groupby(["year","county_fips","party"]).sum().reset_index(level=[0,1]).sort_values("county_fips")

data["votes_rep"]=data_rep.candidatevotes.to_list()
data["ratio"]=data.candidatevotes/(data.candidatevotes+data.votes_rep)
print(data)
with open("geojson_counties.json", 'r') as file:
    geojson=json.load(file)

plot=px.choropleth(
            data_frame = data,
            geojson=geojson,
            locations = "county_fips",
            color="ratio",
            scope = "usa",
            color_continuous_scale=["#ef553b", "#636efa"],
            #hover_data = ["county_name","candidate"],
            template = "plotly_dark",
            animation_frame="year",
            animation_group="county_fips"
        )

plot.write_html("temp.html")