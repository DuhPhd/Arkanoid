import os

# constants
WIDTH = 800
HEIGHT = 800
SIZE = (WIDTH, HEIGHT) # window size in pixels
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FRAMES_PER_SECOND = 60 # number of frames to limit the processing to. Controls global speed
SOURCE_DIR = os.path.split(os.path.abspath(__file__))[0]
IMAGE_DIR = r'images'
SOUND_DIR = r'sounds'

# default Counter parameters
TEXT_FONTSIZE = 48
TEXT_FONTCOLOR = WHITE
TEXT_FONTNAME = 'Arial'

# Score parameters
SCORE_START = 0
SCORE_COLOR = WHITE
SCORE_INCREMENT = 1
SCORE_POS = (0.1, 0.07)
SCORE_SIZE = 36
S_LABEL_TEXT = 'Score'
S_LABEL_POS = (0.1, 0.02)
S_LABEL_SIZE = 20
S_LABEL_COLOR = WHITE

# Time parameters
TIMER_START = 0 # Leave at 0 unless stages offer no time 
TIMER_COLOR = WHITE
TIMER_SPEED = -1 # number of deductions per second
TIMER_POS = (0.9, 0.07)
TIMER_SIZE = 36
T_LABEL_TEXT = 'Time'
T_LABEL_POS = (0.9, 0.02)
T_LABEL_SIZE = 20
T_LABEL_COLOR = WHITE

# stage name parameters
NAME_POS = (0.5, 0.05) # position of stage name as proportino of screen size
NAME_COLOR = WHITE

# divider for score, etc
DIV_POS = 0.1 # position of divider for score etc as proportion of vertical screen size
DIV_WIDTH = 4 # width of divider in number of pixels
DIV_COLOR = WHITE

# Paddle parameters
USER_SPEED = 700 # speed in pixels per second, converted to pixels per frame
USER_SPRITE = os.path.join(SOURCE_DIR, IMAGE_DIR, r'paddle.png')
USER_BALL_MINANGLE = 30 # minimum angle (in degrees) ball bounces off paddle when on the very ede of the paddle
USER_BALL_MAXANGLE = 90 # maximum angle (in degrees) ball bounces off paddle when in the center of the paddle

# Ball parameters
BALL_SPEED = 700 # speed in pixels per second, converted to pixels per frame
BALL_SPRITE = os.path.join(SOURCE_DIR, IMAGE_DIR, r'ball.png')
BALL_SOUND = os.path.join(SOURCE_DIR, SOUND_DIR, r'ball_hit.wav')
BALL_POS = (0.5, 0.95) # starting position of ball in proportion of screen/frame

# default Brick parameters
BRICK_SPRITE = os.path.join(SOURCE_DIR, IMAGE_DIR, r'brick.gif')

# default Stage parameters
STAGE_BG = BLACK # default is always a color tuple
STAGE_NAME = 'stage' # default name
STAGE_NUM = 1 # default order number
STAGE_TIME = 120 # default time for the stage
STAGE_DIR = r'stages' # folder that stages can be found in relative to SOURCE_DIR
STAGE_FILE = r'config' # name of stage configuration file including extension inside STAGE_DIR
STAGE_CONFIG_DELIM = ' ' # delimiter for stage config file
STAGE_CONFIG_COMMENT = '#' # string for comments in stage config file
STAGE_CONFIG_NAME = 'name' # stage name config keyword
STAGE_CONFIG_NUM = 'number' # stage number config keyword
STAGE_CONFIG_BG = 'background' # stage background config keyword
STAGE_CONFIG_BRICK = 'brick' # stage brick config keyword
STAGE_CONFIG_TIME = 'time' # time to complete stage