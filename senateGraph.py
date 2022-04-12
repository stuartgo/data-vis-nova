import plotly.express as px
from dvis_data import senate_winners
import math
import pandas as pd
def senate_graph(year,senate_winners,color_map):
    
    senate_winners=senate_winners[senate_winners.year<=year]
    senate_winners.sort_values("year",inplace=True,ascending=False)
    senate_data=senate_winners.drop_duplicates(["state"])
    senate_data.seats=senate_data.seats.apply(lambda x:x.split(" ") )
    senate_data.seats=senate_data.seats.apply(lambda x: [x[0],x[0]] if len(x)==1 else x)
    senate_data=senate_data.explode("seats")
    senate_data.sort_values(by=["seats"],inplace=True)
    radiuses=[3,4,5,6,7]
    num_points=[16,18,20,22,24]
    points=[]
    for index,radius in enumerate(radiuses):
        for point_num in range(0,num_points[index]):
            angle=(math.pi/(num_points[index]-1))*point_num
            points.append((math.cos(angle)*radius,math.sin(angle)*radius,radius))
    data=pd.DataFrame(points)
    data.columns=["x","y","party"]
    data.sort_values("x",inplace=True)
    data.party=senate_data["seats_labels"].to_list()
    data["state"]=senate_data["state"].to_list()
    print(data)
    print("here")
    fig = px.scatter(data, x="x", y="y", color="party",hover_data = {"party":True, "state":True,"x":False,"y":False},color_discrete_map=color_map)
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
        visible=False
    )
    fig.update_xaxes(visible=False)
    fig.update_traces(marker_size=15)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title="Party"
    )
    return fig


# senate_graph(2020,senate_winners,{
#             "REPUBLICAN": "red",
#             "DEMOCRAT": "blue",
#             "OTHER": "green"
#         }).write_html("temp.html")
