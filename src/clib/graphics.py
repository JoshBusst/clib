
from typing import List

'''
@brief
Holds sprite information including scale and the path to the sprite
image. Includes some functionality for loading the sprite.
'''
class Sprite:
    def __init__(self, name: str, sprite_path: str, scale: List[int]):
        self.name = name
        self.sprite_path = sprite_path
        self.scale = scale
        self.img = None

    def load(self):
        if self.img != None:
            print(f"Sprite name ->>{self.name}<<- already loaded!")
            return

        if exists(self.sprite_path):
            sprite_img = pygame.image.load( self.sprite_path )
            sprite_img = pygame.transform.scale( sprite_img, self.scale )

            self.img = sprite_img
        else:
            abort("Sprite load failed.")



'''
@brief
Converts a world point or pose into a pixel coordinate.
'''
def world2screen(worldPoint):
    assert(len(worldPoint) in [2, 3])

    # offset the world point
    offset = [dim[0] for dim in WORLD_DIMS_XY]
    offsetPoint = subtract( worldPoint[0:2],  offset )
    screenPoint = multiply( offsetPoint, SCREEN_2_WORLD_RATIO )
    
    # account for pixel coordinate frame (+Xscreen -> left, +Yscreen -> down)
    screenPoint[1] = SCREEN_SIZE[1] - screenPoint[1]

    # handle point or pose inputs
    if len(worldPoint) == 3:
        return roundc(screenPoint) + [worldPoint[2]]
    else:
        return roundc(screenPoint)
 


'''
@brief
Converts a pixel coordinate in to a world point.
'''
def screen2world(screenPoint):
    rawWorldPoint    = divide( screenPoint, SCREEN_2_WORLD_RATIO )
    offsetWorldPoint = add( rawWorldPoint, [dim[0] for dim in WORLD_DIMS_XY] )

    return offsetWorldPoint



'''
@brief
Blits an image from its centre at a given pose. This ensures
sprites are drawn where they are intended and that they rotate
around their centre of mass.
Sprite_ijt uses pixel coordinates and clockwise-positive radians
measured from the upward vertical.
'''
def drawSprite(sprite_name: str, sprite_ijt):
    assert(len(sprite_ijt) == 3)

    # centre image exactly on point
    sprite_img = pygame.transform.rotate( sprites[sprite_name].img, -degrees(sprite_ijt[2]) )
    rect = sprite_img.get_rect()
    rect.center = tuple( sprite_ijt[0:2] )

    # draw image to graphics object
    SCREEN.blit( sprite_img, rect )



'''
@brief
Add a new sprite to the sprites list.
'''
def addSprite(sprite: Sprite):
    sprites[sprite.name] = sprite



'''
@brief
Draws a text string to the console
'''
def drawText(text, text_ij=(0,0), textColour=(0,0,0), fontSize=20):
    font = pygame.font.SysFont('Comic Sans MS', fontSize)
    textSurface = font.render(text, False, tuple(textColour))
    
    SCREEN.blit(textSurface, tuple(text_ij))



'''
@brief

'''
def drawfps(val: float=None):
    if val == None: val = fps

    drawText(f"FPS: {round(val)}")



'''
@brief
Run once per timestep. This function calculates time since it was
last run and produces a dt value used for VFR (variable frame sleep).
The function uses a variable or preset target fps to calculate dt
values.
'''
def delay(t_fps: int=None):
    global start_time, fps_hist, fps

    if t_fps == None: t_fps = target_fps

    target_dt = 1/t_fps
    
    t = time()
    dt = max(0.000001, target_dt - t + start_time)
    start_time = t
    
    fps_hist.pop(0)
    fps_hist.append(1/dt)
    fps = avg(fps_hist)

    return dt



'''
@brief
Flushes the start time tracker. This may be run just prior to entering
the main loop to ensure the first time step calculation is not dependent
on when the graphics module is loaded.
'''
def flushDelay():
    global start_time
    start_time = time()



'''
@brief
Changes the preset fps. System defaults to this value when functions such
as delay() are not given a target fps.
'''
def setTargetfps(fps: int):
    fps = round(fps)

    assert(fps > 0 and fps < 1000)

    global target_fps
    target_fps = fps



'''
@brief
Fills the screen with background colour. Overwrites all drawn graphics.
'''
def clearScreen():
    SCREEN.fill(BACKGROUND_COLOUR)



'''
@brief
Calls to relevant functions to display graphics
that have been draw to the screen.
'''
def updateScreen():
    pygame.display.update()



'''
@brief
Initialises the pygame interface and loads sprites.
'''
def graphicsInit():
    global SCREEN

    if len(sprites.keys()) == 0:
        warning("No sprites found!")
    else:
        # initialise sprites
        for sprite in sprites.values():
            sprite.load()

    # initialise pygame and generate screen handle
    pygame.init()
    SCREEN = pygame.display.set_mode( tuple(SCREEN_SIZE) )
    pygame.display.set_caption(WINDOW_TITLE)
    pygame.font.init()



'''
@brief
Packs down and closes the pygame interface.
'''
def graphicsClose():
    pygame.quit()





##### Define package fields #####
import pygame
from lib import absc, warning, abort, roundc, zeros, avg
from os.path import exists
from numpy import add, subtract, multiply, degrees, pi, divide
from time import time


# screen parameters
SCREEN_SIZE = [1000, 500]
WINDOW_TITLE = "ENTER TITLE"
BACKGROUND_COLOUR = [210, 210, 210]


# user-defined world dimensions (uneven "screen:world size" ratio will warp graphics)
WORLD_DIMS_XY = [[-15, 15], # [xmin, xmax]
                 [ 0,  500]] # [ymin, ymax]


# ratio for mapping world coordinates to screen pixel coordinates
SCREEN_2_WORLD_RATIO = [SCREEN_SIZE[0] / ( sum( absc(WORLD_DIMS_XY[0]) )),
                        SCREEN_SIZE[1] / ( sum( absc(WORLD_DIMS_XY[1]) ))]
    

# warn user if screen ratios are inconsistent
if SCREEN_2_WORLD_RATIO[0] != SCREEN_2_WORLD_RATIO[1]:
    warning("Screen ratio is uneven. X: %.2f, Y: %.2f\n" %(*SCREEN_2_WORLD_RATIO,)+
            "This may lead to warped graphics.")
    

# global graphics objects
sprites = {}
SCREEN  = None
SPRITE_IMGS = []



# timekeeping
fps = 0 # the current fps, sliding window average
target_fps = 35
start_time = time()
fps_hist = zeros(8)





if __name__ == "__main__":
    spritepath = "Dude.png"
    newSprite = Sprite('sprite1', spritepath, (100,150))
    addSprite(newSprite)

    pose = [100,100,pi/4]

    graphicsInit()
    clearScreen()
    drawSprite(sprites[0], pose)
    updateScreen()

    from ui import handleUserInputs
    from time import sleep

    while True:
        response = handleUserInputs()
        # pose = (pose, response)

        clearScreen()
        drawSprite(sprites[0], pose)
        updateScreen()

        sleep(0.02)