from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap
from config import *
import pandas as pd

df = pd.read_csv('citi-bike-history-data.csv',
                 usecols=[
                     "start station name",
                     "start station latitude",
                     "start station longitude"
                 ])

df.columns = ["Station", "Latitude", "Longitude"]
df.drop_duplicates(subset=["Station", "Latitude", "Longitude"], inplace=True)

source = ColumnDataSource(
    data=dict(lat=df.Latitude,
              lon=df.Longitude,
              name=df.Station)
)

map_options = GMapOptions(lat=40.73, lng=-74.05, map_type="roadmap", zoom=14)

p = gmap(GOOGLE_MAPS_API_KEY, map_options, title="Used stations in December 2019", tools="pan", plot_width=800, plot_height=800)

hover = HoverTool()
hover.tooltips = [('Name of the station', '@name')]
p.add_tools(hover)

p.circle(x="lon", y="lat", size=10, fill_color="tomato", fill_alpha=0.8, source=source)

curdoc().add_root(p)
