from math import sqrt, atan, pi
import sys

arm_length = 0.36
header = {"frame": 1, "blueX": 2, "blueY": 3, "yellowX": 5, "yellowY": 6, "pinkX": 8, "pinkY": 9, "greenX":11, "greenY": 12}
to_cook = sys.argv[1]
cook_to = sys.argv[2]
cook_to_polar = sys.argv[3]
name = to_cook.split("/")[-1]

#Steps for cooking
#Determine the center blue node's location
#Center all other nodes
#Normalise the node length
#Determine polar coordinates

def average(points, index):
    agg = 0.0
    count = 0
    for p in points:
        if p[index] > 0:
            agg += p[index]
            count += 1
    
    return agg / count

def average_dist(points, index1, index2):
    agg = 0.0
    count = 0
    for p in points:
        if p[index1] > 0 and p[index2] > 0:
            agg += abs(p[index1] - p[index2])

            count += 1
    
    return (agg / count)

def interpolate(points):
    #Interpolate missing results
    for h in header.values():
        valid = -1
        #Indexes of missing values
        missing = []
        for i in range(len(points)):
            p = points[i][h]

            colour = "_"
            p_size = -1
            for c in header.keys():
                if header[c] == h:
                    colour = c.strip("X").strip("Y")
                
                if "Y" in c and colour in c:
                    p_size = header[c] + 1
                    

            if p > -1 and int(points[i][p_size]) > 2000:
                #There is values to interpolate
                if len(missing) > 0:
                    missing.insert(0, valid)

                    for j in range(len(missing)):
                        index = missing[j]
                        percent = float(j) / float(len(missing))
                        diff = (p - points[valid][h])

                        points[index][h] = points[valid][h] + percent * float(diff)

                    missing = []

                #Track the last valid seen
                valid = i
                    
            #Value missing interpolate later
            else:
                if valid > -1:
                    missing.append(i)

def center_points(points, scale, center, outers):
    for o in outers:
        for i in range(len(points)):
            if points[i][o] > -1:
                points[i][o] = (center - points[i][o]) * scale
            
def polar(x, y):
    dist = sqrt(pow(x, 2) + pow(y, 2))
    angle = atan(abs(x)/(abs(y)+0.0000001)) * 180 / pi
    if x > 0 and y > 0:
        angle = angle
    if x > 0 and y < 0:
        angle = angle
    if x < 0 and y > 0:
        angle = -angle
    if x < 0 and y < 0:
        angle = -angle

    return (dist, angle)

def polarise(points):
    
    polar_points = [] 
    for p in points:
        blue_polar = polar(p[header["blueX"]], p[header["blueY"]])
        yellow_polar = polar(p[header["yellowX"]], p[header["yellowY"]])
        pink_polar = polar(p[header["pinkX"]], p[header["pinkY"]])
        green_polar = polar(p[header["greenX"]], p[header["greenY"]])

        polar_p = []
        polar_p.append(p[header["frame"]])
        polar_p.extend(blue_polar)
        polar_p.extend(yellow_polar)
        polar_p.extend(pink_polar)
        polar_p.extend(green_polar)

        polar_points.append(polar_p)
    
    return polar_points

def write_points(points):
    r = open(cook_to + name, "w")
    r.write("frame,blueX,blueY,yellowX,yellowY,pinkX,pinkY,greenX,greenY\n")
    for p in points:
        line = ""
        for h in header.values():
            line += str(p[h]) + ","
        line = line.strip(",") + "\n"
        r.write(line)
    r.close()

def write_polar_points(points):
    r = open(cook_to_polar + name, "w")
    r.write("frame,blueDist,blueAngle,yellowDist,yellowAngle,pinkDist,pinkAngle,greenDist,greenAngle\n")
    for p in points:
        line = ""
        for h in range(len(p)):
            line += str(p[h]) + ","
        line = line.strip(",") + "\n"
        r.write(line)
    r.close()
         

if __name__ == "__main__":
    f = open(to_cook, "r")

    points = f.readlines()
    f.close()

    try:
        for i in range(len(points)):
            points[i] = points[i].split(",")

            for h in header.keys():
                h = header[h]

                checked = points[i][h]
                checked = checked[:min(len(checked), 10)]

                points[i][h] = float(checked)

        #Finding the blue center
        bluePos = (average(points, header["blueX"]),
                average(points, header["blueY"]))

        average_arm_dist = (average_dist(points, header["blueX"], header["yellowX"])
                            ,average_dist(points, header["blueY"], header["yellowY"]))


        average_arm_dist = sqrt(pow(average_arm_dist[0], 2) + pow(average_arm_dist[1], 2))
        scale = arm_length / average_arm_dist

        interpolate(points)
            
        #Center all the data
        Xheader = [header[x] for x in header.keys() if "X" in x]
        Yheader = [header[y] for y in header.keys() if "Y" in y]

        center_points(points, scale, bluePos[0], Xheader[1:])
        center_points(points, scale, bluePos[1], Yheader[1:])

        center_points(points, scale, bluePos[0], [header["blueX"]])
        center_points(points, scale, bluePos[1], [header["blueY"]])

        polar_points = polarise(points)

        write_points(points)            
        write_polar_points(polar_points)

    except Exception as e:
        print("Exception occurred for file: " + str (to_cook))
        print(e)
        print()