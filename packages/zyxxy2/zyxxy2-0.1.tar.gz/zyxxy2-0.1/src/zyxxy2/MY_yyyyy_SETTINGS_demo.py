########################################################################
## Draw With yyyyy (or yyyyy Drawings, or Drawing With yyyyy)
## (C) 2021 by Yulia Voevodskaya (draw.with.zyxxy@outlook.com)
## 
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  See <https://www.gnu.org/licenses/> for the specifics.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
########################################################################

import numpy as np

demo_screen_zoom = 1

figure_params = {'canvas_width' : 20, 
                 'canvas_height' : 14,
                 'figsize' : np.array([0.5 * 14 / demo_screen_zoom, 0.5 *8 / demo_screen_zoom]),
                 'dpi' : 150 * demo_screen_zoom,
                 'tick_step' : 1,
                 'font_size' : 0.5 * 10/demo_screen_zoom,
                 'widget_lefts' : {'left': 0.21, 'right' : 0.56},
                 'plot_gap' : 0.05,
                 'plot_bottom_gap' : 0.01,
                 'left_right_gap' : 0.0025,
                 'left_right_opacity' : 0.1,
                 'add_width_to_axes_background' : 0.039,
                 'add_height_to_axes_background' : 0.01,
                 'x_axis_label' : "RULER FOR X's", 
                 'y_axis_label' : "RULER FOR Y's"}

my_default_demo_shapes = {"left" : "a_triangle", "right" : "a_square"}

my_default_demo_style = {"left" : {"line"   : {'linewidth' : 5}, 
                                   "patch"  : {'opacity' : 1.0}, 
                                   'outline': {'linewidth' : 5, 'color' : 'yellow'},
                                   'diamond': {"color" : 'red'},
                                   ''       : {"color" : 'red', 'layer_nb' : 1}},
                         "right": {"line"   : {}, 
                                   "patch"  : {'opacity' : 0.5}, 
                                   'outline': {'color' : 'none'}, # default outline width is 0
                                   'diamond': {"color" : 'blue'},
                                   ''       : {"color" : 'blue', 'layer_nb' : 1}}}

demo_style_widgets_value_ranges = {"color"    : ['yellow', 'blue', 'red', 'green', 'none'],
                                   "layer_nb"  : [0, 3, 1, 1],
                                   "linewidth" : [0, 10, 1, 1], 
                                   "opacity"   : [0, 1, 1, 0.1]}