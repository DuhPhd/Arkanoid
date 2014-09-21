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
SCORE_POS = (0.1, 0.05)

# Life parameters
LIFE_START = 0 # leave at 0 unless stages offer no additional lives
LIFE_COLOR = WHITE
LIFE_INCREMENT = -1
LIFE_POS = (0.9, 0.05)

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
STAGE_LIVES = 1 # default number of lives given for the stage
STAGE_DIR = r'stages' # folder that stages can be found in relative to SOURCE_DIR
STAGE_FILE = r'config' # name of stage configuration file including extension inside STAGE_DIR
STAGE_CONFIG_DELIM = ' ' # delimiter for stage config file
STAGE_CONFIG_COMMENT = '#' # string for comments in stage config file
STAGE_CONFIG_NAME = 'name' # stage name config keyword
STAGE_CONFIG_NUM = 'number' # stage number config keyword
STAGE_CONFIG_BG = 'background' # stage background config keyword
STAGE_CONFIG_BRICK = 'brick' # stage brick config keyword
STAGE_CONFIG_LIFE = 'lives' # number of lives for the stage (added to player's current)