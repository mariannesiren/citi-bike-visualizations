from bokeh.layouts import column
from bokeh.plotting import output_file, show, figure
from bokeh.models import HoverTool, Slider, ColorBar
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
import pandas as pd

df = pd.read_csv('citi-bike-history-data.csv', usecols=["tripduration", "start station name"])

grouped_data = df.groupby('start station name')['tripduration'].sum().to_frame().reset_index()

output_file("citi-bike-history-by-station.html")

mapper = linear_cmap(
    field_name='y',
    palette=Spectral6,
    low=min(grouped_data['tripduration'] % 60),
    high=max(grouped_data['tripduration'] % 60)
)

p = figure(
    plot_width=1000,
    plot_height=500,
    x_range=grouped_data['start station name'],
    title="Trip duration minutes in December 2019 from start stations"
)

r = p.circle(grouped_data['start station name'], grouped_data['tripduration'] % 60, line_color=mapper, color=mapper, alpha=0.5)

p.xaxis.major_label_orientation = 1.2

hover = HoverTool()
hover.tooltips = [('Duration', '@y')]
p.add_tools(hover)

slider = Slider(start=0.1, end=2, step=0.01, value=0.3)
slider.js_link('value', r.glyph, 'radius')

color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))
p.add_layout(color_bar, 'right')

show(column(p, slider))