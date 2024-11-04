
from yyyyy_canvas import create_canvas_and_axes, show_and_save
from yyyyy_shape_functions import draw_a_square
from yyyyy_all_EXAMPLES import draw_a_gradient_chessboard

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width=10, canvas_height=10, tick_step=1, model=draw_a_gradient_chessboard)

#######################################################
# Now let's draw the shapes!                         ##
draw_a_square(left=0, bottom=0, side=1, color='black')

show_and_save()