# VINSET
Video inset function

This toolbox provides a commandline function that will insert a graph (defined in a CSV file) into a video 
________________________
# Installation requirements and guide
## Step 1: Python 3.9
If your base python interpreter is version 3.9, you can skip this step.
If not, please create the virtual environment as follow:

If you are using anaconda, please open the `Anaconda Powershell Prompt` and then
```
conda create -n your-environment-name python=3.9
```
```
conda activate your-environment-name
```
If not, please

(FOR LINUX/MAC)

install venv 
```
sudo apt-get install python3.9-venv
```
create virtual my_env_name
```
python3 -m venv my_env_name
```
activate virtual my_env_name
```
source my_env_name/bin/activate
```

(FOR WINDOWS)

install venv
```
py -m pip install --user virtualenv
```
create virtual my_env_name
```
py -m venv my_env_name
```
activate virtual my_env_name
```
.\my_env_name\Scripts\activate
```

## Step 2: Opencv-python
If your base python interpreter is version 3.9,
```
pip install opencv-python --upgrade
```
if not, activate your virtual environment that your created with python version 3.9 and
```
pip install opencv-python --upgrade
```
## Step 3: Install
If it is the first time installation,
```
pip install vinset
```
If it has been installed before,
```
pip install vinset --upgrade
```
_________________________________
# User guide
There are 2 types of vinset image overlay in version 4.0.0 and above which are  
1.  graph overlay  
2.  text overlay  
```
vinset -i input.mp4 [-d gaze.csv] -o output.mp4 -c config.json [-t graph or text] [-tl timeline.json]
```
The argument -d is mandatory in graph overlay and does not require in text overlay.
## Graph Overlay Example usage
```
vinset -i input_video.mp4 -o output_video.mp4 -d gaze.csv -c config.json 
```
(or)  
```
vinset -t graph -i input_video.mp4 -o output_video.mp4 -d gaze.csv -c config.json 
```
The default overlay type of vinset is **graph**. Therefore with or without `-t graph`, it will draw graph overlay
### CSV file format for graph overaly
The configuration file will reference ```data.csv``` which will have format:

```
DataID, CurrentTime, Height, Velocity
1, 0, 0.123, 0.566
1, 0.1, 0.146, 0.232
2, 0.2, 0.157, 0.447
2, 0.3, 0.170, 0.677

...

5, 10.4, 2.321, 0.2442
5, 10.5, 2.324, 0.679
```
DataID column is optional but it can be filter by given config file.


### Example configuration file for graph overlay
#### pim_video_middle.json
```
{ "display": "True",
  "axes" : [ {  "name" : "main",
                "box_title": "Pupil movement",
                "box_title_x_position": 70,
                "box_title_y_position": 20,
                "box_title_color": "red",
                "box_title_font_scale": 0.4,
                "box_color": "red",
                "box_thickness": "1",
                "background" : { "fill":"black", "opacity" : 0.3 },
                "position" :  { "x" : 65, "y" : 56, "width" : 250, "height" : 80 } }],
  "series" : [ { "name"  : "x_nom_graph_line",
                "parent_axes" : "main",
                "line_color": "green",
                "line_thickness": 1,
                "zero_line_display": "False",
                "zero_line_thickness": 1,
                "display_type": "static",
                "t_label"     : "time",
                "t_label_x_position"     : 112,
                "t_label_y_position"     : 100,
                "time_offset": -0.09578,
                "y_label"     : "x_nom",
                "y_label_x_position"     : 15,
                "y_label_y_position"     : 125,
                "label_thickness": 1,
                "label_font_scale": 0.4,
                "t_data": "local_time",
                "y_data": "x_nom",
                "filter": "False",
                "filterBy" : "None",
                "pointer_value": {"Enabled": "True", "Color": "red", "Radius": 3},
                "y-limit" : { "type" : "fixed", "limits" : { "lower" : 0.3, "upper" : 0.6 } },
                "t-limit" : { "type" : "time",  "width" : 10 }}]}
```
### Configuration format explanation for graph overlay

#### display = video will be displayed during producing video if it is true.

#### axes = the information of graph boxes.

1.  name = the name of the axes that will be checked from series information.
2.  box_title = the title of the graph box.
3.  box_title_x_position = the x position of title
4.  box_title_y_position = the y position of title
5.  box_title_color = the color of tile
6.  box_title_font_scale = the font scale of tile
7.  box_color = the color of the box.
8.  box_thickess = the thickness of line of box.
9.  background = the color and opacity of background rectangle box.
10.  position = x cordinate, y coordinate, width and height of the box.

#### series = the information of labels and lines.

1.  name = the name or type of line.
2.  parent_axes = the name of parent axes to be called.
3.  line_color = the color of data line.
4.  line_thickness = the color of data line thickess.
5.  zero_line_display = the zero level line will be displayed if it is true and it is actually within lower and upper limit.
6.  zero_line_thickess = the thickess of zero line
7.  display_type = the display type of line. It can be "pen" or "static". If it is "pen", it will be drawn with time. If it is "static", the whole line will be displayed within time scale.
8.  t_label = the label name for time/x axis.
9.  t_label_x_position = x position of the time label. The bigger the number, the closer to the right of the graph box.
10. t_label_y_position = y position of the time label. The bigger the number, the closer to the bottom of the the graph box.
11. time_offset = time difference in milliseconds between start time of gaze.csv and left_right_combined.video. (This `time_offset` is optional and if it is not included, it will be zero.)
12.  y_label_x_position = x position of the y label. The bigger the number, the closer to the left of the graph box.
13. y_label_y_position = y position of the y label. The bigger the number, the closer to the top of the the graph box.
14.  label_thickess = the thickess of label.
15.  label_font_scale = the font scale of label.
16.  t_data = the column name of csv file for time/ x axis data.
17.  y_data = the column name of csv file for y axis data
18.  filter = it will filter "DataID" column if it is true.
19.  filterBy = the column name of csv file and the value to be used to filter. eg. "DataID=4"
20.  pointer_value = the color and radius information of pointer whether it is enabled or not.
21.  y-limit = type and limits of y axis
22.  t-limit = type and width of time/x axis

#### Note: 
1.  Color information can be tuple string eg. "(0,0,255)" or 6 hex color code eg. "#ffffff" or basic color strings which are "red", "green", "blue", "yellow", "black", "white" and "magenta".
2.  Zero line will be displayed if it is enabled and it is actually can be drawn according to the lower limit and upper limit. eg. If lower limit is 1 and upper limit is 2, zero line cannot be drawn.  

## Text Overlay Example usage  
```
vinset -t text -i input_video.mp4 -o output_video.mp4 -c config.json -tl timeline.json
```
The argument -t and -tl are mandatory in text overlay.  

### Example configuration file for text overlay
#### logmar_level_right_bottom.json  
```
{ "display": "True",
  "text_info": {
    "text_marker": "event_marker",
    "text_marker_location": "event->event->logmar_level",
    "text_color": "green",
    "text_font_size":  0.7,
    "text_thickness": 2,
    "time_marker": "timestamp",
    "time_marker_location": "event->timestamp->pts_time",
    "va_logmar_interval": 0.02,
    "minimum_va_decimal": 2
  },
  "stimulus_text_display_location": {"x": 550, "y": 500},
  "va_text_display_location": {"x": 550, "y": 530}
}
```
### Configuration format explanation for text overlay

#### display = video will be displayed during producing video if it is true.

#### text_info = the information of text.

1.  text_marker = the name of event marker to be captured in timeline.json file.
2.  text_marker_location = the directory indicator string of where text marker is located in timeline.json.
3.  text_color = the color of text.
4.  text_font_size = the font size of text.
5.  text_thickness = the pixel thickness of the text.
6.  time_marker = the name of time marker to be captured in timeline.json file.
7.  time_marker_location = the directory indicator string of where time marker is located in timeline.json.
8.  va_logmar_interval = the incremental or decremental step of logmar display for va level.
9.  minimum_va_decimal = the minimum decimal place of logmar display for va level.

#### stimulus_text_display_location = the display location of stimulus level text.

#### va_text_display_location = the display location of va level text.

#### Note: 
`text_color` information can be tuple string eg. "(0,0,255)" or 6 hex color code eg. "#ffffff" or basic color strings which are "red", "green", "blue", "yellow", "black", "white" and "magenta".


_________________________________
# Version upgrade guide
## To check the version of currently installed
```
vinset --version
```
## To upgrade the vinset to latest version
```
pip install vinset --upgrade
```
