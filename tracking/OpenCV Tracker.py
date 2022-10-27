import cv2
import numpy as np
from scipy import ndimage




imageWidth = 1080
imageHeight = 1920

windowWidth = 500
windowHeight = 500

nodeTrails = None



# Define bounds for node colours.
# This will be used to create the mask

blueLowerLimit = np.array([90,70,50]) # setting the blue lower limit
blueUpperLimit = np.array([139,255,255]) # setting the blue upper limit

greenLowerLimit = np.array([65,50,50]) # setting the blue lower limit
greenUpperLimit = np.array([85,255,255]) # setting the blue upper limit

yellowLowerLimit = np.array([14, 140, 150])
yellowUpperLimit = np.array([24, 255, 255])

pinkLowerLimit = np.array([160, 130, 90])
pinkUpperLimit = np.array([165, 255, 255])

#pinkLowerLimit = np.array([161, 140, 90])
#pinkUpperLimit = np.array([164, 255, 255])  

redLowerLimit = np.array([170, 40, 40])
redUpperLimit = np.array([180, 255, 255])

bronzeLowerLimit = np.array([12, 50, 10])
bronzeUpperLimit = np.array([45, 255, 255])




def center(mask):

    # Calculate center point.

    labels, nlabels = ndimage.label(mask)
    
    greenCenter = ndimage.center_of_mass(mask, labels, np.arange(nlabels) + 1 )

    # calc sum of each label, this gives the number of pixels belonging to the blob
    maskSize = ndimage.sum(mask, labels, np.arange(nlabels) + 1 )
    
    # print the center of mass of the largest blob
    try:
        centerCoords = greenCenter[maskSize.argmax()] # notation of output (y,x)
    except ValueError:
        return (-1, -1, 0)

    y = centerCoords[0]
    x = centerCoords[1]

    return x, y, int(maskSize[0])

    



for recording in range(263, 275):


    n = 0
 
    dataFile = open("extractedData-"+str(recording)+".csv", "w")
    dataFile.close()

    dataFile = open("extractedData-"+str(recording)+".csv", "a")

    cap = cv2.VideoCapture("footage-r2/C0" + str(recording) + ".MP4")

    print("Reading", recording, cap)

    while True:
        
        
        ret, frame = cap.read() # Read the frame.
        # 'ret' will return a 1 if frame exists else 0


        # Flip frame vertically:
        frame = cv2.flip(frame, 0)

        # Crop the frame
        # [top:bottom, left:right]

        try:
            frame = frame[500:1400, 80:1000]
        except TypeError:
            break


        # Change color format from BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        # Creat the mask using inRange() function
        # This will produce an image where the color of the objects
        # falling in the range will turn white and rest will be black

        blueMask = cv2.inRange(hsv, blueLowerLimit, blueUpperLimit)
        yellowMask = cv2.inRange(hsv, yellowLowerLimit, yellowUpperLimit)
        pinkMask = cv2.inRange(hsv, pinkLowerLimit, pinkUpperLimit)
        greenMask = cv2.inRange(hsv, greenLowerLimit, greenUpperLimit)

        redMask = cv2.inRange(hsv, redLowerLimit, redUpperLimit)
        bronzeMask = cv2.inRange(hsv, bronzeLowerLimit, bronzeUpperLimit)
        

        greenX, greenY, greenSize = center(greenMask)
        yellowX, yellowY, yellowSize = center(yellowMask)
        pinkX, pinkY, pinkSize = center(pinkMask)
        blueX, blueY, blueSize = center(blueMask)

 
        # Give colour to the mask.
        
        blue = cv2.bitwise_or(frame, frame, mask=blueMask)
        yellow = cv2.bitwise_or(frame, frame, mask=yellowMask)
        pink = cv2.bitwise_or(frame, frame, mask=pinkMask)
        green = cv2.bitwise_or(frame, frame, mask=greenMask)

        red = cv2.bitwise_or(frame, frame, mask=redMask)
        bronze = cv2.bitwise_or(frame, frame, mask=bronzeMask)


        #cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('image', windowWidth, windowHeight)
        #cv2.imshow('image', frame) # to display the original frame


        showNodes = blue
        showNodes = cv2.add(showNodes, yellow)
        showNodes = cv2.add(showNodes, green)
        showNodes = cv2.add(showNodes, pink)

        arms = cv2.add(bronze, red)

        cv2.circle(showNodes, (int(greenX), int(greenY)), 3, (0, 255, 0), 3)
        cv2.circle(showNodes, (int(blueX), int(blueY)), 3, (255, 0, 0), 3)
        cv2.circle(showNodes, (int(yellowX), int(yellowY)), 3, (0, 255, 255), 3)
        cv2.circle(showNodes, (int(pinkX), int(pinkY)), 3, (100, 100, 255), 3)
        

        cv2.namedWindow("det", cv2.WINDOW_NORMAL)

        cv2.resizeWindow('det', windowWidth, windowHeight)
        
        if (n == 0):
            nodeTrails = showNodes

        nodeTrails = cv2.addWeighted(nodeTrails, 1, showNodes, 0.4, 0)

        display = cv2.addWeighted(nodeTrails, 1, arms, 0.5, 0)
        
        cv2.imshow('det', display) # to display the blue object output
        #cv2.imshow('det', nodeTrails) # to display the blue object output
        #cv2.imshow('det', showNodes) # to display the blue object output


        data = (str(recording)+","+str(g)+","+
                str(blueX)+","+str(blueY)+","+str(blueSize)+","+
                str(yellowX)+","+str(yellowY)+","+str(yellowSize)+","+
                str(pinkX)+","+str(pinkY)+","+str(pinkSize)+","+
                str(greenX)+","+str(greenY)+","+str(greenSize)+"\n")

        #print(data)

        if cv2.waitKey(1)==27:
            break

  
        dataFile.write(data)

        n = n + 1

        
    cap.release()
     
    cv2.destroyAllWindows()

    dataFile.close()

print("Done")

