import json

def transformJSONSIntoObjects(arr):
    mObjects = []
    for mFile in arr:
        x = json.loads(mFile)
        mObjects.append(x)
    mObjects.sort(key=lambda x: x['name'], reverse=False)
    return mObjects
