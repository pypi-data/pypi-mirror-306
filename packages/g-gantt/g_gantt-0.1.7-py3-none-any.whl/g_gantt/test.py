from main import *
from datetime import datetime

# Initialize the chart with a title
chart = Chart("Example Chart")

chart.add_task("T1","Label for Task 1", date(2024,10,1), date(2024,10,15), resource="Epic1")

chart.add_task("T2","Label for Task 2", duration = 1.5, dependencies="T1",resource = "Epic1")

chart.add_task("T3","Label for Task 3", duration = 1.2, dependencies="T2", resource = "Epic1",)

chart.add_task("T4","Label for Task 4", duration = 1.5, dependencies="T3", resource = "Epic1")

chart.add_task("T5","Label for Task 5", duration = 2.5, dependencies="T4", resource = "Epic1")

chart.add_task("T6","Label for Task 1", date(2024,10,12), date(2024,10,28), resource="Epic2")

chart.add_task("T7","Label for Task 5", duration = 2.5,resource = "Epic2")



# Customize the background color!
chart.set_background_color("B4B4B4")

# Enable Critical Path Highlighting
chart.set_critical_path(True)

# Set the chart dimensions!
chart.set_dimensions(1500,1000)

# Show the chart in your browser!
chart.show()

# Save the html code for the chart!
chart.save('gantt_chart_critical_path.html')
