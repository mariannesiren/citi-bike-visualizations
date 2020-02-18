from bokeh.plotting import output_file, show, figure
from bokeh.models import ColumnDataSource, HoverTool, ColorBar
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
import pandas as pd

df = pd.read_csv('citi-bike-history-data.csv', usecols=["tripduration", "starttime"])

output_file("trip-durations-by-date.html")

grouped_data = df.groupby('starttime')['tripduration'].sum().to_frame().reset_index()

mapper = linear_cmap(
    field_name='top',
    palette=Spectral6,
    low=min(grouped_data['tripduration'] % 60),
    high=max(grouped_data['tripduration'] % 60)
)

p = figure(
    title="Trip duration minutes in December 2019",
    plot_width=800,
    x_range=grouped_data['starttime']
)

p.vbar(x=grouped_data['starttime'], top=grouped_data['tripduration'] % 60, width=0.9,  line_color=mapper, color=mapper)

p.y_range.start = 0
p.x_range.range_padding = 0.05
p.xaxis.major_label_orientation = 1.2

hover = HoverTool()
hover.tooltips = [('Trip duration', '@top')]
p.add_tools(hover)

color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))
p.add_layout(color_bar, 'right')

show(p)