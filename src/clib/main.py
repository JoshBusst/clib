from time import sleep, time
from lib import psleep
from graphics import *
from physics import *
from ui import *


sprite = Sprite('sprite1','Dude.png',[150,150])
addSprite(sprite)
graphicsInit()

body = RigidBody(1,1)
body.constrainForces(15)
body.addGravity()


while True:
    clearScreen()
    drawSprite(sprite.name, world2screen(body.state.getPos()))
    drawfps()
    updateScreen()

    response = handleUserInputs()
    forces = r2f_2DTD(body, response)

    dt = delay(35)

    updateAccelerations(body, forces)
    updateState(body.state, dt)

    psleep(dt)
