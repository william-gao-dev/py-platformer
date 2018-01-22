# Game options and files

# Global variables
TITLE = "Skyward!"
WIDTH = 480
HEIGHT = 600
FPS = 60

# Player properties
PLAYER_ACC = .5
PLAYER_FRICTION = -.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -20 # Velocity change on the negative Y axis on player jump event

# Starting platforms
PLATFORM_LIST = [


(0,HEIGHT-40,WIDTH,40),
(WIDTH/2-50, HEIGHT*3/4,100,20),
(125,HEIGHT-350,100,20),
(350,200,100,20),
(175,100,50,20)


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
