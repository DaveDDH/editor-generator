import os
from DBUtils import saveToDB, retrieveFromDB
import shutil

def readAllFilesInDiskDir(directory, type):
    dsstore = ".DS_Store"
    dssLen = len(dsstore)
    mFiles = []
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            fileName = os.path.join(root, name)
            fnLen = len(fileName)
            if fileName.find(dsstore) != fnLen - dssLen:
                if type == "*" or fileName.find(type) == fnLen - len(type):
                    f1 = open(fileName, 'r')
                    mFiles.append(f1.read())
                    f1.close()
    return mFiles

def listAllFilesInDiskDir(directory, type):
    dsstore = ".DS_Store"
    dssLen = len(dsstore)
    mFiles = []
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            fileName = os.path.join(root, name)
            fnLen = len(fileName)
            if fileName.find(dsstore) != fnLen - dssLen:
                if type == "*" or fileName.find(type) == fnLen - len(type):
                    mFiles.append(fileName)
    return mFiles

def readFileFromDisk(fileName):
    file = open(fileName, 'r')
    data = file.read()
    file.close()
    return data

def writeFileToDisk(mPath, name, data):
    mFile = os.path.join(mPath, name)
    os.makedirs(os.path.dirname(mPath), exist_ok=True)
    f = open(mFile, 'w+')
    f.write(data)
    f.close()

def createDirInDisk(path, name):
    mPath = os.path.join(path, name)
    if not os.path.exists(mPath):
        os.mkdir(mPath)
        return mPath
    elif debug:
        shutil.rmtree(mPath)
        return createDirInDisk(path, name)
    else:
        return False

def listAllFilesFromList(mList):
    mFiles = []
    for item in mList:
        if item.find('/*') == len(item) - 2:
            mFiles += listAllFilesInDirRecursively(item[:-2])
        else:
            mFiles.append(item)
    return list(dict.fromkeys(mFiles))

def listAllFilesInDirRecursively(dir):
    mFiles = listAllFilesInDiskDir(dir, '*')
    return mFiles

def copyFile(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)

from ConfigUtils import getAllProperties

properties = getAllProperties()
debug = False

if "debugMode" in properties.keys():
    if properties["debugMode"] == "True":
        debug = True