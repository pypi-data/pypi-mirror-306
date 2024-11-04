from yyyyy_utils import full_turn_angle
from MY_yyyyy_SETTINGS_demo import figure_params

canvas_width = figure_params['canvas_width']
canvas_height = figure_params['canvas_height']
half_min_size = min(canvas_width, canvas_height) / 2

slider_range = {
  'half_min_size': [0., half_min_size,
                    int(half_min_size / 2), 1],
  'plus_minus_half_min_size':
  [-half_min_size, half_min_size,
   int(half_min_size / 2), .1],
  'half_min_size_34': [0., half_min_size,
                       int(half_min_size * 3 / 4), 1],
  'half_width': [0., canvas_width, int(canvas_width / 2), 1],
  'half_height': [0., canvas_height,
                  int(canvas_height / 2), 1],
  'stretch': [-3, 3, 1, 0.1],
  'from_0_to_5': [0., 5, 1, 0.1],
  'from_0_to_1': [0., 1, 0.6, 0.05],
  '5_to_50': [5, 50, 10, 5],
  'turn': [0, full_turn_angle, 0, full_turn_angle / 12],
  'double_turn': [0, 2 * full_turn_angle, 0, full_turn_angle / 12],
  'long_turn': [0, 5 * full_turn_angle, 0, full_turn_angle / 4],
  'half_turn': [0, full_turn_angle / 2, 0, full_turn_angle / 12],
  'quarter_turn': [0, full_turn_angle / 4, 0, full_turn_angle / 12],
  'vertices': [1, 12, 5, 1],
}