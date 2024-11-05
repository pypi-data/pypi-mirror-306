# Created by: Brady Golomb
#
# Last Modified by: Brady Golomb
#
# Maintained by: 
# Brady Golomb
#
#

from datetime import datetime, date, timedelta
import json
import webbrowser
import os
import tempfile

class Chart:
    """
    A class to represent a Gantt Chart

    Attributes:
    tasks : list
        A list of tasks to be displayed on the chart.
    title : str
        The title of the chart.
    categories : list
        A list of categories for the Gantt chart.
    options : dict
        A dictionary for chart options like background color and Gantt chart arrow properties.
    """

    def __init__(self, title: str):
        """
        Constructs all the necessary attributes for the Chart object.

        Args:
            title (str): The chart title
        """
        self.tasks = []
        self.title = title
        self.categories = []
        self.options = {
            "backgroundColor": {"fill": "white"},
            "gantt": {
                "arrow": {
                    "angle": 45,
                    "color": "#000",
                    "length": 8,
                    "radius": 15,
                    "spaceAfter": 4,
                    "width": 1.4,
                },
                "barCornerRadius": 2,
                "criticalPathEnabled": False,
                "criticalPathStyle": {"stroke": "#e64a19", "strokeWidth": 5},
                "innerGridHorizLine": {"stroke": "#ccc", "strokeWidth": 1},
                "innerGridTrack": {"fill": "#f3f3f3"},
                "innerGridDarkTrack": {"fill": "#e0e0e0"},
                "labelMaxWidth": 300,
                "percentEnabled": True,
                "shadowEnabled": True,
                "shadowColor": "#000",
                "shadowOffset": 1,
                "sortTasks": True,
                "trackHeight": None
            },
            "width": 1500,
            "height": 1000
        }

    def add_task(
            self, 
            task_id: str, 
            task_label: str, 
            start: date = None, 
            end: date = None,
            duration: float = None, 
            dependencies: str = None, 
            resource: str = None, 
            percent_complete: int = 0
            ):  
        """
        Adds a task to a Gantt Chart,
        Need start and end, end and duration, or start and duration

        Args:
            title (str): The chart title
        """    
        
        # Calculate end only if duration is provide

        if (start and end):
            task = {
                "Task ID": task_id,
                "Task Name": task_label,
                "Start": start,
                "End": end,
                "Duration": None,
                "Percent Complete": percent_complete,
                "Dependencies": dependencies or [],
                "Resource": resource
            }
            self.tasks.append(task)
        elif (start and duration):
            task = {
                "Task ID": task_id,
                "Task Name": task_label,
                "Start": start,
                "End": None,
                "Duration": duration,
                "Percent Complete": percent_complete,
                "Dependencies": dependencies or [],
                "Resource": resource
            }
            self.tasks.append(task)
        elif (end and duration):
            task = {
                    "Task ID": task_id,
                    "Task Name": task_label,
                    "Start": None,
                    "End": end,
                    "Duration": duration,
                    "Percent Complete": percent_complete,
                    "Dependencies": dependencies or [],
                    "Resource": resource
                }
            self.tasks.append(task)
        elif duration:
            task = {
                    "Task ID": task_id,
                    "Task Name": task_label,
                    "Start": None,
                    "End": None,
                    "Duration": duration,
                    "Percent Complete": percent_complete,
                    "Dependencies": dependencies or [],
                    "Resource": resource
                }
            self.tasks.append(task)
        else:
            print("Needs 2 out of 3 (Start, End, Duration)")

        

    def set_option(self, option_path, value):
        """Set a specific option in the chart options."""
        # Use dot notation for nested option paths (e.g., 'gantt.arrow.color')
        keys = option_path.split(".")
        option = self.options
        for key in keys[:-1]:
            option = option.setdefault(key, {})
        option[keys[-1]] = value

    def set_dimensions(self, width, height):
        self.options["width"] = width
        self.options["height"] = height

    def set_background_color(self, color):
        self.options["backgroundColor"]["fill"] = color

    def set_critical_path(self, t_or_f:bool):
        self.options["gantt"]["criticalPathEnabled"] = t_or_f

    def get_tasks(self):
        return self.tasks

    def get_options(self):
        return self.options
    
    def format_value(self, value, column_name=None):
        if value is None:
            return 'null'
        elif isinstance(value, (datetime, date)):
            return f'new Date({value.year}, {value.month - 1}, {value.day})'
        elif column_name == 'Duration':
            # Format the duration as daysToMilliseconds(x)
            return str(value*24*60*60*1000)
        elif isinstance(value, list):
            # Join list elements into a comma-separated string
            return json.dumps(','.join(value))
        elif isinstance(value, str):
            return json.dumps(value)
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return json.dumps(str(value))



    def get_html(self):
        # Prepare the data rows
        data_rows = []

        for task in self.tasks:
            formatted_row = '[' + ', '.join(self.format_value(
                task.get(col, None), col) for col in [
                'Task ID', 'Task Name', 'Resource', 'Start', 'End',
                'Duration', 'Percent Complete', 'Dependencies']) + ']'
            data_rows.append(formatted_row)

        data_rows_str = ',\n        '.join(data_rows)

        # Prepare the resources (categories) and their colors
        options = {
            'height': self.options["height"],
            'width': self.options["width"],
        }

        options_json = json.dumps(options)

        # Generate the HTML content
        html_content =f'''<!DOCTYPE html>
<html>
<head>
    <title>{self.title}</title>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
    google.charts.load('current', {{'packages':['gantt']}});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {{
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Task ID');
        data.addColumn('string', 'Task Name');
        data.addColumn('string', 'Resource');
        data.addColumn('date', 'Start Date');
        data.addColumn('date', 'End Date');
        data.addColumn('number', 'Duration');
        data.addColumn('number', 'Percent Complete');
        data.addColumn('string', 'Dependencies');


        data.addRows([
        {data_rows_str}
        ]);

        var options = {options_json};

        var chart = new google.visualization.Gantt(document.getElementById('chart_div'));

        chart.draw(data, options);
    }}
    </script>
</head>
<body>
    <h1 style="text-align: center;">{self.title}</h1>
    <div id="chart_div"></div>
</body>
</html>
        '''

        return html_content

    def show(self):
        html_content = self.get_html()
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            f.write(html_content)
            filename = f.name
        webbrowser.open('file://' + os.path.realpath(filename))

    def save(self, filename):
        html_content = self.get_html()
        with open(filename, 'w') as f:
            f.write(html_content)