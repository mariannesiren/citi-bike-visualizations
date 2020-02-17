from bokeh.plotting import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap
from config import *
import pandas as pd

df = pd.read_csv('citi-bike-history-data.csv',
                 usecols=["start station name", "start station id", "start station latitude", "start station longitude"]
                 )

# Create tuples from dataframe
geocode_tuples = [tuple(x) for x in df.to_numpy()]

# Remove duplicates
uniq_geocodes = list(set([i for i in geocode_tuples]))

# Seems that values are always ordered in tuples, so we can for now trust that
# - the of the station is the first value
# - id is the second value
# - latitude is always the third value
# - longitude is the fourth value in tuple
station_name = [i[0] for i in uniq_geocodes]
latitudes = [i[2] for i in uniq_geocodes]
longitudes = [i[3] for i in uniq_geocodes]

output_file("gmap.html")

map_options = GMapOptions(lat=40.73, lng=-74.05, map_type="roadmap", zoom=14)

p = gmap(GOOGLE_MAPS_API_KEY, map_options, title="Start stations")

source = ColumnDataSource(
    data=dict(lat=latitudes,
              lon=longitudes,
              name=station_name)
)

hover = HoverTool()
hover.tooltips = [('Name of the station', '@name')]
p.add_tools(hover)

p.circle(x="lon", y="lat", size=10, fill_color="tomato", fill_alpha=0.8, source=source)

show(p)