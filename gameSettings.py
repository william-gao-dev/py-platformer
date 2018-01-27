# Game options and files

# Global variables
TITLE = "Skyward!"
WIDTH = 550
HEIGHT = 750
FPS = 70
LASTWIDTH = 0

# Player sprite properties
PLAYER_ACC = .5
PLAYER_FRICTION = -.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -20 # Velocity change on the negative Y axis on player jump event
WALKFRAME_DELAY = 200
IDLEFRAME_DELAY = 300

# Game properties
BOOST_POWER = 60 # How far powerup will boost
BOOST_SPAWN_PCT = 10 # How likely powerup will spawn.

# Starting platforms
PLATFORM_LIST = [


(0,HEIGHT-60),
(WIDTH/2-50, HEIGHT*3/4),
(125,HEIGHT-350),
(350,200),
(175,100),
(355,414)


]

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (0,155,155)
BGCOLOR = LIGHTBLUE

# Assets
FONT_NAME = 'arial' # Default font
HIGHSCORE_FILE = 'highscore.txt' # Number will hold a high score
SPRITESHEET = "spritesheet_jumper.png"

# Sounds
JUMP_SOUND = 'jump.wav'
JUMP_SOUND_VOLUME = 0.03

AMBIENT_SOUND = 'musicalt1.wav'
AMBIENT_SOUND_VOLUME = 0.07

START_SCREEN_VOLUME = 0.07
START_SCREEN_MUSIC = 'startscreen.wav'

BOOST_POWERUP_SOUND1 = "boost_start.wav"
BOOST_POWERUP_VOLUME1 = 0.20

BOOST_POWERUP_SOUND2 = "boost_stop.wav"
BOOST_POWERUP_VOLUME2 = 0.2
