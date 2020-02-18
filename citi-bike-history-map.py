from bokeh.plotting import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap
from config import *
import pandas as pd

# Stations on map -->
df_start_stations = pd.read_csv('citi-bike-history-data.csv',
                                usecols=[
                                    "start station name",
                                    "start station id",
                                    "start station latitude",
                                    "start station longitude"
                                ])

df_end_stations = pd.read_csv('citi-bike-history-data.csv',
                              usecols=[
                                  "end station name",
                                  "end station id",
                                  "end station latitude",
                                  "end station longitude"
                              ])

# Create tuples from start station dataframe
tuples_start_stations = [tuple(x) for x in df_start_stations.to_numpy()]

# Create tuples from end station dataframe
tuples_end_stations = [tuple(x) for x in df_end_stations.to_numpy()]

# Join start station tuples and end station tuples
station_tuples = tuples_end_stations + tuples_start_stations

# Remove duplicates
uniq_stations = list(set([i for i in station_tuples]))

# Seems that values are always ordered in tuples, so we can for now trust that
# - the of the station is the first value
# - id is the second value
# - latitude is always the third value
# - longitude is the fourth value in tuple
station_name = [i[0] for i in uniq_stations]
latitudes = [i[2] for i in uniq_stations]
longitudes = [i[3] for i in uniq_stations]

output_file("gmap.html")

map_options = GMapOptions(lat=40.73, lng=-74.05, map_type="roadmap", zoom=14)

p = gmap(GOOGLE_MAPS_API_KEY, map_options, title="Used stations in December 2019")

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
