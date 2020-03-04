from bokeh.layouts import column, row, layout
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, Slider, GMapOptions, DaysTicker
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.plotting import gmap
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
from config import *
import pandas as pd
import numpy as np

# Read data from csv
df = pd.read_csv('citi-bike-history-data.csv', usecols=[
    "tripduration",
    "starttime",
    "start station name",
    "start station latitude",
    "start station longitude"
])

df.columns = ["Tripduration", "Station", "Starttime", "Latitude", "Longitude"]
df['Starttime'] = pd.to_datetime(df['Starttime'])

# Plot trip duration minutes by start time
grouped_data_by_start_time = df.groupby(df['Starttime'].dt.date)['Tripduration'].sum().to_frame().reset_index()

mapper_top = linear_cmap(
    field_name='top',
    palette=Spectral6,
    low=min(grouped_data_by_start_time['Tripduration'] % 60),
    high=max(grouped_data_by_start_time['Tripduration'] % 60)
)

plot_by_starttime = figure(
    title="Trip duration minutes in December 2019",
    plot_width=800,
    plot_height=620,
    x_axis_type='datetime'
)

start_time = pd.to_datetime(grouped_data_by_start_time['Starttime'])

plot_by_starttime.vbar(
    x=pd.to_datetime(grouped_data_by_start_time['Starttime']),
    top=grouped_data_by_start_time['Tripduration'] % 60,
    width=0.9,
    line_color=mapper_top,
    color=mapper_top,
    line_width=4
)

plot_by_starttime.xaxis.ticker = DaysTicker(days=np.arange(1, 32))
plot_by_starttime.xaxis.formatter = DatetimeTickFormatter(days=["%d, %b %Y"])
plot_by_starttime.y_range.start = 0
plot_by_starttime.xaxis.major_label_orientation = 1.2
plot_by_starttime.toolbar_location = None

color_bar = ColorBar(color_mapper=mapper_top['transform'], width=8,  location=(0,0))
plot_by_starttime.add_layout(color_bar, 'right')


# Plot trip duration minutes by start station
grouped_data_by_start_station = df.groupby('Station')['Tripduration'].sum().to_frame().reset_index()

mapper_y = linear_cmap(
    field_name='y',
    palette=Spectral6,
    low=min(grouped_data_by_start_station['Tripduration'] % 60),
    high=max(grouped_data_by_start_station['Tripduration'] % 60)
)

plot_by_station = figure(
    plot_width=1000,
    plot_height=700,
    x_range=grouped_data_by_start_station['Station'],
    title="Trip duration minutes in December 2019 from start stations"
)

r_by_station = plot_by_station.circle(grouped_data_by_start_station['Station'], grouped_data_by_start_station['Tripduration'] % 60, line_color=mapper_y, color=mapper_y, alpha=0.5)

plot_by_station.xaxis.major_label_orientation = 1.2
plot_by_station.toolbar_location = None

hover = HoverTool()
hover.tooltips = [('Duration', '@y')]
plot_by_station.add_tools(hover)

slider = Slider(start=0.1, end=2, step=0.01, value=0.3)
slider.js_link('value', r_by_station.glyph, 'radius')

color_bar = ColorBar(color_mapper=mapper_y['transform'], width=8,  location=(0,0))
plot_by_station.add_layout(color_bar, 'right')


# Map with stations
df.drop_duplicates(subset=["Station", "Latitude", "Longitude"], inplace=True)

source = ColumnDataSource(
    data=dict(lat=df.Latitude,
              lon=df.Longitude,
              name=df.Station)
)

map_options = GMapOptions(lat=40.73, lng=-74.05, map_type="roadmap", zoom=14)

map = gmap(GOOGLE_MAPS_API_KEY, map_options, title="Used stations in December 2019", tools=["pan", "tap"], plot_width=970, plot_height=800, toolbar_location=None)

hover = HoverTool()
hover.tooltips = [('Name of the station', '@name')]
map.add_tools(hover)

map.circle(x="lon", y="lat", size=10, fill_color="tomato", fill_alpha=0.8, source=source)

# Output plots
doc_layout = layout(column(map, row(column(plot_by_station, slider), plot_by_starttime)))
curdoc().add_root(doc_layout)

