
from typing import List
from math import radians, pi


'''
NOTE
Theta is measured clockwise-positive from the upward-facing vertical.
'''

'''
@brief
The 2D state variable. Includes pose and pose derivatives for use in complex,
time-dependent movement calculations.
'''
class State:
    def __init__(self,
                 pos = [0, 0, 0],
                 vel = [0, 0, 0],
                 acc = [0, 0, 0]):
        
        # always assumes units of metres and radians
        [self.x,  self.y,  self.theta] = pos
        [self.vx, self.vy, self.omega] = vel
        [self.ax, self.ay, self.alpha] = acc

    def getPos(self):
        return [self.x, self.y, self.theta]
    
    def getVel(self):
        return [self.vx, self.vy, self.omega]
    
    def getAcc(self):
        return [self.ax, self.ay, self.alpha]
    
    def getx(self):
        return [self.x, self.vx, self.ax]
    
    def gety(self):
        return [self.y, self.vy, self.ay]
    
    def getAng(self):
        return [self.theta, self.omega, self.alpha]
    
    def printState(self):
        from lib import roundList

        pos = roundList(self.getPos(), 1)
        vel = roundList(self.getVel(), 1)
        acc = roundList(self.getAcc(), 1)

        print(f"\n\n\n{pos}\n{vel}\n{acc}")



'''
@brief

'''
class RigidBody:
    def __init__(self, mass: float=None, I: float=None):
        self.mass  = mass # mass
        self.I     = I    # mass moment of inertia
        self.gravity = 0

        self.state = State()
        self.maxRotForce = None
        self.maxLinForce = None
    
    def getInertia(self):
        return self.mass * squaredDist(self.state.vx, self.state.vy)
    
    def getRotInertia(self):
        return self.I * self.state.omega

    def addGravity(self):
        self.gravity = 9.81

    def constrainForces(self, maxLinForce: float=5, maxRotForce: float=10):
        self.maxLinForce = maxLinForce
        self.maxRotForce = maxRotForce



'''
@brief

'''
class Drone(RigidBody):
    def __init__(self):
        RigidBody.__init__(self)
        
        # thrust and angle limiters
        self.maxThrust = 20
        self.minThrust = 0

        self.maxTheta = pi/4 # max turn angle [rad]
        self.maxOmega = pi/2 # max turning velocity [rad/s]
        self.maxAlpha = pi   # max turning acceleration [rad/s^2]

        # friction
        self.minLinearVelocity  = 0.6 # below this speed threshold, the drone will stop
        self.minAngularVelocity = radians(15) # below this threshold, the drone will stop rotating



'''
@brief
SUVAT maths function. Takes distance, velocity acceleration and time
to calculate new distance and velocity values.
'''
def suvat(params, dt):
    [s0, v0, a0] = params

    s = s0 + v0*dt + 0.5*a0*dt**2
    v = v0 + a0*dt

    return [s, v]



'''
@brief
Updates position and velocity states from SUVAT equations. Includes
bouncy collision physics and static friction logic.
'''
def updateState(state: State, dt, minLinearVelocity=0.15, minAngularVelocity=pi/8):
    from graphics import WORLD_DIMS_XY

    # calculate state update from current state
    [state.x,     state.vx]    = suvat(state.getx(), dt)
    [state.y,     state.vy]    = suvat(state.gety(), dt)
    [state.theta, state.omega] = suvat(state.getAng(), dt)


    # add drag on velocity parameters
    state.vx    -= linearDragCoeff * state.vx    * dt
    state.omega -= angDragCoeff    * state.omega * dt


    # static friction stops the drone below a certain velocity if acceleration is 0
    if abs(state.vx)    < minLinearVelocity  and state.ax    == 0: state.vx    = 0
    if abs(state.omega) < minAngularVelocity and state.alpha == 0: state.omega = 0


    # enforce position and angle limits and additional padding for graphics, and add y offset 
    w = add(WORLD_DIMS_XY, screenPadding * array([[1, -1],[1, -1]]))
    [xmin, xmax] = w[0]
    [ymin, ymax] = w[1]

    state.x = clip( state.x, xmin, xmax )
    state.y = clip( state.y, ymin, ymax )
    state.theta = wrapToPi(state.theta)


    # bouncy collision logic
    if   state.x == xmin:  state.vx =  bouncePercent*abs(state.vx)
    elif state.x == xmax:  state.vx = -bouncePercent*abs(state.vx)

    if   state.y == ymin:  state.vy =  bouncePercent*abs(state.vy)
    elif state.y == ymax:  state.vy = -bouncePercent*abs(state.vy)



'''
@brief
Response to force - 2D top down. This function takes a response vector
and rigid body, and calculates relevant x, y, and angular forces. Can
be repurposed for sideview worlds by applying an additional gravity
calculation externally.
'''
def r2f_2DTD(body: RigidBody, response) -> List[float]:
    f_lin = (response[0] - response[1]) * body.maxLinForce
    f_rot = (response[3] - response[2]) * body.maxRotForce

    f_x = f_lin * sin(body.state.theta)
    f_y = f_lin * cos(body.state.theta) - body.gravity * body.mass

    return [f_x, f_y, f_rot]



'''
@brief
Updates only the acceleration values (ax, ay, alpha) in the state
matrix based on input thrust values.

@input forces
This is a list containing 3 values: the x force, the y force and
the rotational torque active on the body.
'''
def updateAccelerations(body: RigidBody, forces: list):
    body.state.ax    = forces[0] / body.mass
    body.state.ay    = forces[1] / body.mass
    body.state.alpha = forces[2] / body.mass



'''
@brief
Returns the squared distance from [0, 0] to point [x, y].
'''
def squaredDist(x, y):
    return sqrt(x**2 + y**2)



### environment constants
g = 9.81
bouncePercent   = 0.2 # % of velocity that rebounds when colliding with a wall
linearDragCoeff = 0.6 # drag
angDragCoeff    = 0.4 # drag

# position padding to ensure moving body graphics remain on screen
screenPadding = 0.8 # metre



from numpy import sqrt, sin, cos, add, array
from lib import wrapToPi, clip


if __name__ == "__main__":
    print(squaredDist(1, 1))