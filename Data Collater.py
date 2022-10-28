import math
import os

# Data format:
dataFormat = ("Recording,Time,Type,InitAngle,AddedMass,LateStart,"+
              "BlueX,BlueY,BlueAngle,BlueDist,"+
              "YellowX,YellowY,YellowAngle,YellowDist,"+
              "PinkX,PinkY,PinkAngle,PinkDist,"+
              "GreenX,GreenY,GreenAngle,GreenDist\n")

cookedDataFiles = []

for root, dirs, files in os.walk("./cooked_data/"):
    for name in files:
        filepath = os.path.join(root, name)
        print(filepath)
        cookedDataFiles.append(filepath)

print("Found " + str(len(cookedDataFiles)) + " data files.")



runData = []

runDataFile = open("runs.csv")


def findRecordingFiles(recordingNum):

    polar = None
    norm = None

    for file in cookedDataFiles:
        if recordingNum in file:
            if "polar" in file:
                polar = file
            else:
                norm = file

            if norm != None and polar != None:
                return norm, polar



print("\n")


theDataFile = open("allData.csv", "w")
theDataFile.close()

theDataFile = open("allData.csv", "a")

theDataFile.write(dataFormat)


for line in runDataFile.readlines():

    runFile, runType, initCond, lateStart = line.split(",")

    if runType not in ["angle", "mass", "propagation"]:
        continue

    recording = runFile[2:]
    lateStart = lateStart[:-1]

    try:
        normFilename, polarFilename = findRecordingFiles(recording)
    except TypeError:
        continue


    # Calculate initial conditions.

    initAngle = "45"
    addedMass = "0"
    
    if "mass" in runType:
        addedMass = initCond
    else:
        initAngle = initCond

    if "prop" in runType:
        runType = "prop"

        
    
 
    # Read frame by frame run data

    normFile = open(normFilename)
    polarFile = open(polarFilename)

    normData = normFile.readlines()
    polarData = polarFile.readlines()

    print(len(normData), len(polarData))

    normFile.close()
    polarFile.close()
    

    for frameIndex in range(0, len(normData)):

        frameNo, blueDist, blueAngle, yellowDist, yellowAngle, pinkDist, pinkAngle, greenDist, greenAngle = polarData[frameIndex].split(",")

        frameNo, blueX, blueY, yellowX, yellowY, pinkX, pinkY, greenX, greenY = normData[frameIndex].split(",")

        greenY = greenY[:-1]
        greenAngle = greenAngle[:-1]

        frameNo = frameNo.split(".")[0]

        #print(frameNo)

        if "frame" in frameNo:
            continue
        
        now = str(int(frameNo) / 120)

        dataString = (recording+","+now+","+runType+","+initAngle+","+addedMass+","+lateStart+","+
              blueX+","+blueY+","+blueAngle+","+blueDist+","+
              yellowX+","+yellowY+","+yellowAngle+","+yellowDist+","+
              pinkX+","+pinkY+","+pinkAngle+","+pinkDist+","+
              greenX+","+greenY+","+greenAngle+","+greenDist+"\n")

        theDataFile.write(dataString)





    print(recording, normFile, runType, initCond, lateStart)

            
            

    


theDataFile.close()
runDataFile.close()





