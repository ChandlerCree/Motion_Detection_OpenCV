"""Please read README.md"""

from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
import pandas

#Sets "Start" and "End" columns in df to datetime objects
df["Start"] = pandas.to_datetime(df["Start"])
df["End"] = pandas.to_datetime(df["End"])

#Standardizes the format of the datetime object
df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

#Generates the figure and sets the height/width to scalable
#various other plot graphical changes
p=figure(x_axis_type='datetime', height=100, width=500, sizing_mode="scale_width", title="Motion Graph")
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.desired_num_ticks=1

#Standardizes way to provide data to bokeh plot
cds=ColumnDataSource(df)

#Displays Start and End time when hovering over sections in bokeh plot
hover=HoverTool(tooltips=[("Start: ", "@Start_string"),("End: ", "@End_string")])
p.add_tools(hover)

#Generates a rectangle at the 'Start' and 'End' times
q=p.quad(left="Start", right="End", bottom=0, top=1, color="green", source=cds)

#Writes the html file in the below filepath
output_file("output/graphs/Graph.html")

#Displays the bokeh plot in a browser
show(p)