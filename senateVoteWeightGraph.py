
import plotly.express as px
import pandas as pd
  
df = pd.DataFrame(["NY"])
df.columns=["locations"]
plot = px.scatter_geo(df, locations="locations")



plot.write_html("temp.html")