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

screen_zoom = 1/2

# There are 148 beautiful pre-defined colors!
# You can find them here:
# https://matplotlib.org/stable/gallery/color/named_colors.html
#
# If this is not enough,
# you can save your favourite colors here!
# Try to give them names different from ...
# ... the names of standard colors
my_color_palette = {'superBlue'   : '#648fff',
                     'superViolet' : '#785ef0',
                     'superPink'   : '#dc267f',
                     'superOrange' : '#fe6100',
                     'superGold'   : '#ffb000',

                     'DarkTeal'   : "#004949",
                     'SeaWave'    : "#009292",
                     'BubblePink' : "#ff6db6",
                     'LightPink'  : "#ffb6db",
                     'Purple'     : "#490092",
                     'RoyalBlue'  : "#006ddb",
                     'Hyacinth'   : "#b66dff",
                     'PastelBlue' : "#6db6ff",
                     'LightBlue'  : "#b6dbff",
                     'Burgundy'   : "#920000",
                     'MidBrown'   : "#924900",
                     'LightBrown' : "#db6d00",
                     'BrightGreen': "#24ff24",
                     'Yellow'     : "#ffff6d"}

my_default_diamond_size = 0.015 
default_outlines_width = 5 
default_extreme_layer_nb = 1001    

# colors, alphas and linewidths!
my_default_color_etc_settings = {
                     "line" : {'color' : 'black', 
                               'linewidth' : 2, 
                               'joinstyle' : 'straight', 
                               'layer_nb' : 1,
                               "capstyle" : 'straight'}, 
                     "patch" : {'opacity' : 1.0, 
                                'layer_nb' : 1, 
                                'color' : 'none'},
                     "outline" : {'color' : 'black', 
                                  'linewidth' : 0, 
                                  'joinstyle' : 'straight', 
                                  'layer_nb' : 1},
                     "diamond" : {'color' : 'none', #  None #
                                  'opacity' : 1.0,
                                  'layer_nb' : default_extreme_layer_nb}}

# Font sizes and adjustment needed to fit them
my_default_font_sizes = {'title'      : 16/screen_zoom/2,
                         'axes_label' : 12/screen_zoom/2,
                         'axes_tick'  : 8/screen_zoom/2}

# Figure sizes (in inches) and DPIs  
# Figure size in pixels is DPI * figure size in inches

my_default_display_params = {'max_figsize' : [4.5/screen_zoom, 3.5/screen_zoom],
                             'min_margin' : 0.25/screen_zoom,
                             'title_pad' : 3.5/screen_zoom,
                             'x_axis_label' : "RULER FOR X's", 
                             'y_axis_label' : "RULER FOR Y's"}

my_default_image_params = {'dpi'     : 200*screen_zoom,
                           'format'  :'png'}

my_default_animation_params = {'dpi'     : 70,
                               'interval': 1000/24,
                               'blit'    : True,
                               'repeat'  : False,
                               'FPS'     : 24,
                               'writer'  : 'ffmpeg',
                               'format'  : 'mp4'}

my_default_images_folder = "images_videos"

my_default_text_bubble_params = {'color' : 'black',
                                 'background_color' : 'white',
                                 'linewidth' : 0,
                                 'linecolor' : 'black',
                                 'fontsize' : 12/screen_zoom, 
                                 'verticalalignment' : 'bottom',
                                 'horizontalalignment' : 'left', 
                                 'multialignment' : 'left',
                                 'wrap' : True,
                                 'pad' : 0.3, 
                                 # 'rounding_size' : 0,
                                 'fontfamily' : 'monospace', 
                                 'color' : 'black',
                                 'opacity' : 1, 
                                 'layer_nb' : 1,
                                 'triangle_width' : 5}
                                 