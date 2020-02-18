from bokeh.plotting import output_file, show, figure
from bokeh.models import ColumnDataSource, HoverTool
import pandas as pd

df = pd.read_csv('citi-bike-history-data.csv', usecols=["tripduration", "starttime"])

output_file("trip-durations-by-date.html")

grouped_data = df.groupby('starttime')['tripduration'].sum().to_frame().reset_index()

p = figure(
    title="Trip duration minutes in December 2019",
    plot_width=800,
    x_range=grouped_data['starttime']
)

p.vbar(x=grouped_data['starttime'], top=grouped_data['tripduration'] % 60, width=0.9)

p.y_range.start = 0
p.x_range.range_padding = 0.05
p.xaxis.major_label_orientation = 1.2

hover = HoverTool()
hover.tooltips = [('Trip duration', '@top')]
p.add_tools(hover)

show(p)