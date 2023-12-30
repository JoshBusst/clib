
from typing import List

'''
@brief
User interface data container. Contains key logs and
response metrics calculation parameters.
'''
class UserInterface:
    def __init__(self):
        self.arrowKeys = [pygame.K_UP,
                          pygame.K_DOWN,
                          pygame.K_LEFT,
                          pygame.K_RIGHT]
        
        self.historySize = 6
        self.keyLog = [zeros(self.historySize) for i in range(4)] # 4xN list of binary arrow key status flags

        linearRange = divide( list(range(self.historySize)), 10 )
        self.responseVector = multiply(linearRange, linearRange) # time-scaled exponential response vector
        self.responseScalar = sum(self.responseVector) # scales output response to a percentage

    '''
    @brief
    Uses the internal keyLog register to calculate time-scaled
    response metrics from user inputs.
    '''
    def getResponse(self):
        keyStrengths = zeros(4)

        # iterate key history to generate time-scaled response outputs
        # NOTE: last entry is most significant/newest
        for i in range(4):
            keyHist = self.keyLog[i]

            # apply quick stop logic. History will be zeroed once button is released
            if keyHist[-1] == 0:
                self.keyLog[i] = zeros(self.historySize)
            else:
                # normalise keystrength calcualted from history and response vector
                keyStrengths[i] = sum(multiply(keyHist, self.responseVector)) / self.responseScalar

        return keyStrengths

    '''
    @brief
    Logs key list parameter to the internal key flag register
    '''
    def logKeys(self, keys):
        for i in range(4):
            self.keyLog[i].append(keys[i])

            # clip size of key log
            if len(self.keyLog[i]) > self.historySize:
                self.keyLog[i] = self.keyLog[i][1:]





'''
@brief
Nonblocking function to get keys currently held. Logs
keys for time-scaled input response.
'''
def getArrKeysHeld():
    # determine keys held and calculate drone response
    keyLog      = pygame.key.get_pressed()
    keysPressed = list(keyLog[key] for key in UI.arrowKeys)

    UI.logKeys(keysPressed)

    return keysPressed



'''
@brief
Handles arrow key and quit events.
Keys are returned as a list in order of UP, DOWN, LEFT, RIGHT.
'''
def handleUserInputs():

    # quit conditions
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            graphicsClose()
            exit()


    # generate response percentages from keylog 
    getArrKeysHeld()
    response = UI.getResponse()
    
    return response



'''
@brief
Flush the inputs queue and give the window a chance
to be respositioned. Only responds to quit conditions.
'''
def flushUserInputs():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            consoleClose()
            exit()



import pygame
from numpy import multiply, divide
from lib import zeros
from graphics import graphicsClose



UI = UserInterface()


if __name__ == "__main__":
    pass