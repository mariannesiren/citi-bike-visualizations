from bokeh.plotting import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
from config import *
import pandas as pd

df = pd.read_csv('citi-bike-history-data.csv',
                 usecols=["start station id", "start station latitude", "start station longitude"]
                 )

# Seems that values are always ordered in tuples, so we can for now trust that the id is the first value
# in tuple, latitude is always the second value in tuple and longitude is the third value in tuple
geocode_tuples = [tuple(x) for x in df.to_numpy()]
uniq_geocodes = list(set([i for i in geocode_tuples]))

latitudes = [i[1] for i in uniq_geocodes]
longitudes = [i[2] for i in uniq_geocodes]

output_file("gmap.html")

map_options = GMapOptions(lat=40.73, lng=-74.05, map_type="roadmap", zoom=14)

p = gmap(GOOGLE_MAPS_API_KEY, map_options, title="Start stations")

source = ColumnDataSource(
    data=dict(lat=latitudes,
              lon=longitudes)
)

p.circle(x="lon", y="lat", size=10, fill_color="tomato", fill_alpha=0.8, source=source)

show(p)