import plotly.express as px

import math
import pandas as pd
print("shits")
def senate_graph(year,senate_winners,color_map):
    
    senate_winners=senate_winners[senate_winners.year<=year]
    senate_winners.sort_values("year",inplace=True,ascending=False)
    print("schmixx")
    print(senate_winners)
    senate_data=senate_winners.drop_duplicates(["state"])

    senate_seats_data=senate_data.seats.apply(lambda x:x.split(" ") )
    senate_seats_data=senate_seats_data.apply(lambda x: [x[0],x[0]] if len(x)==1 else x)
    senate_seats_data=senate_seats_data.explode()
    senate_seats_data.sort_values(inplace=True)
    radiuses=[3,4,5,6,7]
    num_points=[16,18,20,22,24]
    points=[]
    for index,radius in enumerate(radiuses):
        for point_num in range(0,num_points[index]):
            angle=(math.pi/(num_points[index]-1))*point_num
            points.append((math.cos(angle)*radius,math.sin(angle)*radius,radius))
    data=pd.DataFrame(points)
    data.columns=["x","y","color"]
    data.sort_values("x",inplace=True)
    data.color=senate_seats_data.to_list()

    fig = px.scatter(data, x="x", y="y", color="color",color_discrete_map=color_map)
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
    )
    return fig