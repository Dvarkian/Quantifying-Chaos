import PySimpleGUI as sg # GUI Manager.
import numpy as np
import cv2 
import time
import random


# Size of the map (image).
canvas_size = (600, 600) # [px]

# Size of the window.
window_size = (800, 800) # [px]


# Crop parameters for video [px]
base = 1130
top = 3100
left = 150
right = 2000

mapCenter = ((right+left)/2, (top+base)/2)

bgCol = "grey15"

# Define layout for window.
layout = [[sg.Graph(canvas_size, (left, base), (right, top), background_color = "grey5", k="-MAP-")],
          [sg.Text("Run: -1", key="-RUN-", background_color=bgCol),
           sg.Text("Frame: -1", key="-FRAME-", background_color=bgCol),
           sg.Text("Time: -1s", key="-TIME-", background_color=bgCol)]]


# Init. Window.
window = sg.Window("Quantifying Chaos", layout,
                   background_color=bgCol,
                   finalize=True,
                   margins=(10, 10))



run = "205"

window["-RUN-"].update("Run " + str(run))

cap = cv2.VideoCapture("footage/C0" + run + ".MP4")



# Determine starting frame.

fps = 24

startTime = 0

startTimesFile = open("startTimes.txt", "r")

runType = "normal"

for line in startTimesFile.readlines():
    if run in line:
        startTime = float((line.split(",")[1]).strip(" "))

        if "r" in line:
            runType = "prop"
        if "m" in line:
            runType = "mass"
        break
else:
    runType = "mass"

startFrame = int(fps * startTime)

startTimesFile.close()


# converst rgb colour to hex code.
def rgb2hex(rgb):
    return '#%02x%02x%02x' % rgb


# Finds greatest differance between 2 colours.
def greatest_dif(r, g, b):

    greatest = max([abs(r - g),
                    abs(r - b),
                    abs(b - g)])

    return greatest



# Finds distance between 2 points.
def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5



# Finds average coordinate of a set of points.
def avgPt(points):

    x = 0
    y = 0

    for i in points:
        x += i[0]
        y += i[1]

    return (x / len(points), y / len(points))


#Finds lagest range of a set of points.
def spread(points):

    x_min = float("inf")
    x_max = float("-inf")
    y_min = float("inf")
    y_max = float("-inf")
    
    for i in points:
        x_min = min(x_min, i[0])
        y_min = min(y_min, i[1])

        x_max = max(x_max, i[0])
        y_max = max(y_max, i[1])

    return max((x_max - x_min), (y_max - y_min))




frontPts = []

originNodePts = []

n = -1

# List of zones to exclude from consideration.
# [(top left), (bottom right)]
badZones = [[(1020, 2050), (1080, 1850)], # Shaft.
            [(1790, 1510), (2100, 100)] # Box
            ]

if 1:#runType == "normal":
    badZones.append([(370, 1680), (620, 1510)])# Powerpoint.


# Check if a point is in a bad zone.
def inBadZone(point):
    for zone in badZones:
        if (point[0] > zone[0][0] and # Left
            point[0] < zone[1][0] and # Right
            point[1] < zone[0][1] and # Top
            point[1] > zone[1][1] # Base.
            ):

            return True

    return False


started = False

while True: # Main loop

    n += 1 # Count frames analysed.

    if not started:
        window["-FRAME-"].update("Frame: " + str(n), text_color="red")
    else:
        window["-FRAME-"].update("Frame: " + str(n), text_color="green1")

    window["-TIME-"].update("Time: " + str(n/fps)[:6] + "s", text_color="yellow")

    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        window.close()
        break;

    # Read next frame.
    ret, frame = cap.read()

    if not started:
        if n % 4 != 0:
            continue


    # Trim video.
    if (n < startFrame):
        continue

    blueTargets = []

    # Draw exclusion zones.
    for zone in badZones:
        window["-MAP-"].draw_rectangle(zone[0], zone[1], None, "red", 1)
    
    # Draw previous node positions.
    for pt in range(0, len(frontPts)):

        # Draw previous position.
        window["-MAP-"].draw_circle(frontPts[pt], 15, None, "light blue", 1)
        
        if pt > 0:
            #Draw connecting line.
            window["-MAP-"].draw_line(frontPts[pt], frontPts[pt-1], "light blue", 1)
            
        window.refresh()





    #for j in range(base, top, 2): # bottom, top

    # Iterate through all pixels.
    for j in range(top, base, -2):

        # Check for blue sleeve in image.
        if len(blueTargets) < 1000:
            started = 1
        else:
            started = 0
            break
        
        for i in range(left, right, 2): # left, right

            # Get RGB colour of this pixel.
            b = int(frame[j, i][0])
            g = int(frame[j, i][1])
            r = int(frame[j, i][2])

            if inBadZone((i, j)):
                if (random.randint(1, 5) == 1):
                    col = rgb2hex((r, g, b)) # Get colour as hex value
                    #window["-MAP-"].draw_point((i, j), size = 15, color =col)
                    
                continue

            

            # Ignore all shades of grey.
            if greatest_dif(r, g, b) > 15:
                # Too low will cause too much white to show.
                # 16 too high
                # 11 too low

                # Ignore very bright pixels.
                if sum([r, g, b]) < 150 * 3:

                    # Only draw a selection of the pixels alnalysed.
                    if (random.randint(1, 5) == 1):
                        
                        col = rgb2hex((r, g, b)) # Get colour as hex value
                        
                        #window["-MAP-"].draw_point((i, j), size = 15, color =col)

                        

                    # Select for blue pixels.
                    if b - max([r, g]) > 13:
                        # Too high will result in false negatives.
                        # Too low will cause false positives.
                        # 16 too high

                        hshift = 15
                        vshift = 15

                        b_left = int(frame[j, i-hshift][0])
                        g_left = int(frame[j, i-hshift][1])
                        r_left = int(frame[j, i-hshift][2])

                        b_dn = int(frame[j-vshift, i][0])
                        g_dn = int(frame[j-vshift, i][1])
                        r_dn = int(frame[j-vshift, i][2])

                        #window["-MAP-"].draw_circle((i, j), 35, None, "dark green", 1)

                        # Check that nearby pixels are also blue.
                        if b_left - max([r_left, g_left]) > 10:

                            window["-MAP-"].draw_circle((i, j), 45, None, "maroon", 1)

                            blueTargets.append((i, j))
                                              

                    window.refresh()

    #print(blueTargets)


    if not started:
        window["-MAP-"].erase()
        continue

    
    tracked = False # Stores if an unblured node was successfully tracked.
            

    if len(blueTargets) != 0: # Blue node(s) were identified.

        # Triggers selection if only 1 node found.
        blueTargets.append((0, 0))

        # 3 dimensional array to group blue targets by node.
        blueCenters = [[blueTargets[0]]]

        # Nodes found so far.
        nodeIndex = 0

        # Targes found on current node.
        thisNodeCount = 0

        # Iterate through targes identified.
        for target in blueTargets:

            # If target near previous target.
            # Don't consider previous target if it was in a bad zone
            if (dist(target, avgPt(blueCenters[nodeIndex])) < 30 or
                inBadZone(avgPt(blueCenters[nodeIndex]))):
                # 10 too low

                # Consider target on node.
                thisNodeCount = thisNodeCount + 1

                # Ignore nodes with too few targets.
                if thisNodeCount > 2:
                    # 10 too high
                    # 1 too low

                    #window["-MAP-"].draw_circle(target, 40, None, "blue", 3)

                    # Add target to node.
                    blueCenters[nodeIndex].append(target)

                    
            # Target far from previous target.
            elif dist(target, avgPt(blueCenters[nodeIndex])) > 80:

                # We now have all targets that may be assigned to previous node.
                # Nowe to check if previous node was valid.

                #window["-MAP-"].draw_circle(target, 105, None, "yellow", 1)

                # Ignore 'nodes' that appear too spread out.
                if spread(blueCenters[nodeIndex]) < 50:

                    # Find center of node.
                    center = avgPt(blueCenters[nodeIndex])

                    #window["-MAP-"].draw_circle(target, 85, None, "orange", 1)

                    valid = True

                    # Ignore nodes near center at start of run.
                    if n < startFrame + fps:
                        
                        window["-MAP-"].draw_circle(mapCenter, 650, None, "pink", 1)
                        
                        if dist(mapCenter, center) < 650:
                            valid = False

                    print(valid)

                    if valid: # Node is far from center at start of run.


                        
                        if len(frontPts) > 0: # Not first node.

                            # Check that new node is close to previous node.
                            if dist(frontPts[-1], center) < 400:
                        
                                frontPts.append(center)
                                tracked = True

                            elif inBadZone(frontPts[-1]):
                                frontPts.append(center)
                                tracked = True
                                
                        else: # First node to be found.

                            
                            frontPts.append(center)
                            tracked = True

                        if tracked:
                            window["-MAP-"].draw_circle(center, 125, None, "purple", 1)

                            

                    window.refresh()

                nodeIndex = nodeIndex+1
                thisNodeCount = 0

                blueCenters.append([target])


            # Target neither close to nor sufficiently far from previous target.
            else:
                pass



    if not tracked: # Find bluest in radius.

        if len(frontPts) > 0:

            searchRange = 210 # Radius to search for bluest point.

            bluest = float("-inf") # Will store blueness of bluest point in search
            best = (0, 0) # Will store bluest point location in search.

            # Define bounds for search.
            lowerBound = int(frontPts[-1][1]-searchRange)
            upperBound = int(frontPts[-1][1]+searchRange)
            leftBound = int(frontPts[-1][0]-searchRange)
            rightBound = int(frontPts[-1][0]+searchRange)

            window["-MAP-"].draw_rectangle((leftBound, upperBound), (rightBound, lowerBound),
                                           None, "light green", 1)

            window.refresh()

            bs = window["-MAP-"].draw_circle(frontPts[-1], 25, None, "dark blue", 1)

            print("Bounds:", lowerBound, upperBound, leftBound, rightBound)

            for j in range(lowerBound, upperBound, 1): # bottom, top
                for i in range(leftBound, rightBound, 1): # left, right

                    if inBadZone((i, j)):
                        continue
            
                    #print("Target:", i, j)

                    
                    # Exclude points inside square but outside search radius.
                    if dist((i, j), frontPts[-1]) > searchRange:
                        continue

                    if dist((i, j), frontPts[-1]) < 40 and inBadZone((i, j)):
                        continue

                    # Get pixel colour.
                    b = int(frame[j, i][0])
                    g = int(frame[j, i][1])
                    r = int(frame[j, i][2])

                    hshift = 10
                    vshift = 16

                    b_left = int(frame[j, i-hshift][0])
                    g_left = int(frame[j, i-hshift][1])
                    r_left = int(frame[j, i-hshift][2])

                    b_dn = int(frame[j-vshift, i][0])
                    g_dn = int(frame[j-vshift, i][1])
                    r_dn = int(frame[j-vshift, i][2])

                    
                    # Draw a selection of points in radius.
                    if (random.randint(1, 30) == 1):

                        col = rgb2hex((r, g, b))
                        
                        window["-MAP-"].draw_point((i, j), size = 24, color =col)
                        window["-MAP-"].bring_figure_to_front(bs)
                        window.refresh()



                    blueness = b - max([r, g]) + b_left - max([r_left, g_left]) + b_dn - max([r_dn, g_dn])

                    if blueness > bluest:

                        
                        
                        bluest = blueness
                        best = (i, j)

                        window["-MAP-"].relocate_figure(bs, i-12, j+12)
                        window.refresh()

            frontPts.append(best)

    time.sleep(2)

    window["-MAP-"].erase()

    
            
        
