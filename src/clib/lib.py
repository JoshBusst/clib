
from typing import List

'''
@brief
Compares two lists for exact equality.
'''
def isequal(list1, list2):
    list1 = list(list1)
    list2 = list(list2)
    
    if not isinstance(list1, list) or not isinstance(list2, list):
        return False

    if len(list1) != len(list2):
        return False

    # iterate and compare both lists
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False
        
    return True



'''
@brief
Returns rounded number or numeric list accurate to
numDecPoints number of decimal places.
'''
def roundc(x, numDecPoints=0):

    # ensure array is NOT numpy
    x = list(x)

    if isinstance(x, list):
        return [round(val, numDecPoints) for val in x]
    else:
        return round(x, numDecPoints)



'''
@brief
Returns unsigned magnitude(s) of single number or
numeric list.
'''
def absc(x):
    if isinstance(x, list):
        return [abs(val) for val in x]
    else:
        return abs(x)



'''
@brief
Wraps an angle to the range [-pi, pi]. Assumes radians
'''
def wrapToPi(angle):
    return atan2(sin(angle), cos(angle))



'''
@brief
Calculates the shortest distance between two angles relative
to the ang1. ie angdiff(pi, pi/2) will return -pi/2.
'''
def angdiff(ang1, ang2):
    ang = atan2(sin(ang2 - ang1), cos(ang2 - ang1))

    return ang



'''
@brief
This function clips a value to an input domain
'''
def clip(x, xmin, xmax):

    # define nested function for shorthand reuseability
    def clip_integer(val):
        return max(min(val, xmax), xmin)

    # handle list/single input cases
    if isinstance(x, list):
        return [clip_integer(val) for val in x]
    else:
        return clip_integer(x)



'''
@brief
Checks if a value is bounded by the input range
'''
def isbounded(x, xmin, xmax):
    return x >= xmin and x <= xmax



'''
@brief
This function test if two values are within a tolerance
of one another. Good for testing exact values of floats
or checking if points have been reached
'''
def closeto(val1, val2, tol):
    return abs(val1 - val2) < tol



'''
@brief
This function will determine the sign of an integer or list
of integers. Any zero value will return as 0. Does not work
on lists of lists.
'''
def sign(x):

    # declare internal function for reuseability
    def sign_integer(val):
        if val == 0:
            return 0
        elif val < 0:
            return -1
        else:
            return 1
        
    # separeate list or single integer cases
    if isinstance(x, list):
        return [sign_integer(item) for item in x]
    else:
        return sign_integer(x)
        



'''
@brief
Returns a zero vector of input length by default.
Returns a zero matrix when given a column number.
Requires at least one input dimension.
'''
def zeros(dim1: int, dim2: int = 1):
    assert(dim1 > 0 and dim2 > 0)

    if dim2 == 1:
        return [0 for _ in range(dim1)]
    else:
        return [[0 for _ in range(dim1)] for _ in range(dim2)]



'''
@brief
Returns a ones vector of input length by default.
Returns a ones matrix when given a column number.
Requires at least one input dimension.
'''
def ones(dim1: int, dim2: int = 1):
    assert(dim1 > 0 and dim2 > 0)

    if dim2 == 1:
        return [1 for _ in range(dim1)]
    else:
        return [[1 for _ in range(dim1)] for _ in range(dim2)]



'''
@brief
Returns the average of a numeric list.
'''
def avg(lst: List[int]):
    return sum(lst) / len(lst)



'''
@brief
Passing a value to this function will print a debug
message to the console. This message will include the
stack call history, the name of the caller function
that triggered the debug call, and the identifier of
the variable that was passed to the function. Used in
place of a print statement as a cleaner form of 
debugging.
'''
def debug(value):
    from traceback import extract_stack, format_list


    # get a reference to the entire stack call
    stack = extract_stack()


    # get the name of the caller function that triggered the debug call
    # NOTE: there must be at least two values (main file and the debug call)
    # so size is irrelevant
    callerName = stack[-2].name
    printHeading(f"Debug call: {callerName}")


    # get the string identifier of the value that was passed to debug(). ie
    # extract value from within brackets
    startValueName = str(stack[-2].line).index('(') + 1
    valueName = stack[-2].line[startValueName : -1]


    # print the passed value
    print(f"Identifier: {valueName}")
    print(value)
    print()


    # format remaining traceback calls and print
    tracebackMsg = format_list(stack[:-1])
    print('Traceback (most recent call last):')
    print(''.join(tracebackMsg))



'''
@brief
Prints a formatted warning to the console and delays
execution momentarily to draw attention to it.
'''
def warning(string):
    print(f"\n!\n--- Warning ---\n{string}\n!")



'''
@brief
Aborts execution and prints input error string
to the console
'''
def abort(errorMsg):
    print("- Aborting Execution -\n" + \
          "----------------------\n" + \
          errorMsg)
    exit()



'''
@brief
Makes all white pixels in an image transparent.
Static use ONLY.
'''
def removeBackground(imgPath):
    from PIL import Image

    img = Image.open(imgPath)
    img = img.convert('RGBA')
    data = img.getdata()
    newData = []

    for item in data:
        if all([var > 250 for var in item]):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save('droneTransparent.png', "PNG")



'''
@brief
Change colour of an image and save it.
Static use ONLY.
'''
def changeColour(imgPath, colour, i):
    from PIL import Image

    img = Image.open(imgPath)
    data = img.getdata()
    newData = []

    for item in data:
        # if all([(var < 250 and var > 5) for var in item[0:3]]):
        if item[0] < 245 and item[0] > 10:
            newData.append(colour)
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(f"graphics\droneColour{i}.png", "PNG")



'''
@brief
Prints a formatted heading to the console.
'''
def printHeading(heading: str):

    # remove all new lines as this will destroy formatting
    msgCleaned = heading.replace('\n', '')

    # format edges of the message itself
    msgString = f"|   {msgCleaned}   |"

    # generate the bordering string
    headerString = '-'*len(msgString)

    print(f"\n{headerString}\n{msgString}\n{headerString}\n")



'''
@brief
High precision sleep function stolen from StackOverflow. Takes
number of seconds as input and has an approximate accuarcy of
+/- 2ms.
'''
def psleep(duration):
    start_time = perf_counter()

    while True:
        elapsed_time = perf_counter() - start_time
        remaining_time = duration - elapsed_time

        if remaining_time <= 0:
            break

        elif remaining_time > 0.02:  # Sleep for 5ms if remaining time is greater
            sleep(max(remaining_time / 2, 0.0001))  # Sleep for the remaining time or minimum sleep interval
        
        else:
            pass




from math import atan2, sin, cos
from time import sleep, perf_counter


if __name__ == "__main__":
    pass
