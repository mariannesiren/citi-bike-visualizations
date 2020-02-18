from bokeh.plotting import output_file, show, figure
from bokeh.models import ColumnDataSource, Group, HoverTool
import pandas as pd

df = pd.read_csv('citi-bike-history-data.csv', usecols=["tripduration", "start station name"])

grouped_data = df.groupby('start station name')['tripduration'].sum().to_frame().reset_index()

output_file("citi-bike-history-by-station.html")

p = figure(plot_width=1000, plot_height=500, x_range=grouped_data['start station name'])
p.circle(grouped_data['start station name'], grouped_data['tripduration'] % 60, size=10, color="tomato", alpha=0.5)
p.y_range.start = 0
p.xaxis.major_label_orientation = 1.2

hover = HoverTool()
hover.tooltips = [('Duration', '@y')]
p.add_tools(hover)

show(p)
