# This file is regenerated every time you press 'Dump Python File' button
# Rename it if you want to keep the contents

from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_triangle, draw_a_square

create_canvas_and_axes(canvas_width = 20, canvas_height = 14, tick_step = 1)

draw_a_triangle(width = 3.0, height = 3.0, tip_x = 10.0, tip_y = 7.0, color = "red", diamond_color = "red", outline_color = "yellow", outline_linewidth = 5)
draw_a_square(side = 3.0, left = 10.0, bottom = 7.0, color = "blue", diamond_color = "blue", outline_color = "none", opacity = 0.5)

show_and_save()