from clicks import getLines, dispPolar
from lineTools import clean, polList, stepList
from sendingInstructions import sendSteps

#open a window for the user to sketch
a = getLines()

#remove close lines
clean(a)

#get the polar version of the lines
pol = polList(a)

#draw the polar version to check the conversion
#dispPolar(a, pol)

steps = stepList(pol)

sendSteps(steps)



# testData = [
# 	[[150,0],[200,0],[562,0]]
# ]

# #testData = getLines()

# pol = polList(testData)

# print(pol)

# #dispPolar(testData, pol)

# pol = stepList(pol)

# print(pol)

# sendSteps(pol)