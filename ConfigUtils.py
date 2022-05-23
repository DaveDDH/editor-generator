def getAllProperties():
    file = open('./properties.txt', 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    mObject = {}
    for line in data:
        mIndex = line.find('=')
        if mIndex != -1:
            key = line[:mIndex]
            val = line[mIndex + 1:]
            mObject[key] = val
    return mObject