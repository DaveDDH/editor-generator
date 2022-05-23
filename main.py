from ConfigUtils import getAllProperties
from toolGenerator import generate
import sys

args = sys.argv
prevFoundIndex = -1
argsLength = len(args)

requiredArgs = ['output', 'name', 'artifactsDir']
requiredArgsFlag = ['-o', '-n', '-artifactsDir']
mArgs = {}

for i in range(argsLength):
    arg = args[i]
    if arg.find('-o') == 0 and i < argsLength - 1 and i > prevFoundIndex:
        data = args[i + 1]
        prevFoundIndex = i + 1
        mArgs['output'] = data
    if arg.find('-n') == 0 and i < argsLength - 1 and i > prevFoundIndex:
        data = args[i + 1]
        prevFoundIndex = i + 1
        mArgs['name'] = data
    if arg.find('-artifactsDir') == 0 and i < argsLength - 1 and i > prevFoundIndex:
        data = args[i + 1]
        prevFoundIndex = i + 1
        mArgs['artifactsDir'] = data

def checkArgs():
    valid = True
    mKeys = mArgs.keys()
    mLen = len(requiredArgs)
    for i in range(mLen):
        key = requiredArgs[i]
        if not key in mKeys:
            print("ERROR: You must specify the " + key + " with the " + requiredArgsFlag[i] + " argument.")
            valid = False
    return valid

if checkArgs():
    properties = getAllProperties()
    generate(properties, mArgs)
