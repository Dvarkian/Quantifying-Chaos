from curses import COLOR_WHITE
from logging import root
from math import sqrt, atan, pi
from scipy import stats


read_from = "../allData.csv"
write_to = "./energyData.csv"
header = {}
derive_header = {}
run_data = {"223": [], "224": [], "225": [], "226": [], "227":[], "228":[], "229":[], "230":[], "231":[], "233":[], "234":[], "235":[]}

derive_keys = ["Run","Frame","Time",
                  "VelocityY",	"VelocityP", "VelocityG",
                  "AngularY", "AngularP", "AngularG",
                  "CenterYx", "CenterYy", "CenterPx", "CenterPy", "CenterGx", "CenterGy",
                  "TransY", "TransP", "TransG", 
                  "RotateY", "RotateP", "RotateG",
                  "EnergyY", "EnergyP", "EnergyG",
                  "TotalY", "TotalP", "TotalG",
                  "TotalEnergy"]

for i in range(len(derive_keys)):
    derive_header[derive_keys[i]] = i

colours = ["Yellow", "Pink", "Green"]
all_colours = ["Blue", "Yellow", "Pink", "Green"]
time_step = 0.008333

cm_green = 0.38
cm_pink = -0.62
cm_yellow = -0.78

m_green = 0.089
m_pink = 0.232
m_yellow = 0.521
m_arm = 0.144

length = 0.122
arm_length = 2 * length

def polar(x, y):
    dist = sqrt(pow(x, 2) + pow(y, 2))
    angle = atan(abs(x)/(abs(y)+0.0000001)) * 180 / pi
    if x > 0 and y > 0:
        angle = 180 + -angle
    if x > 0 and y < 0:
        angle = angle
    if x < 0 and y > 0:
        angle = -180 + angle
    if x < 0 and y < 0:
        angle = -angle

    return (dist, angle)

def get_root_colour(colour):
    root_colour = ""
    for i in range(len(all_colours)):
        if all_colours[i] == colour:
            root_colour = all_colours[i-1] 
    return root_colour

def get_arm(point, colour):
    root_colour = get_root_colour(colour)

    armx = point[header[colour+"X"]] - point[header[root_colour+"X"]]
    army = point[header[colour+"Y"]] - point[header[root_colour+"Y"]]

    return (armx, army)

def calculate_velocity(derived, data):

    for i in range(1, len(data)):
        
        for c in colours:
            x = c+"X"
            y = c+"Y"
            diffX = (data[i][header[x]] - data[i-1][header[x]]) / time_step
            diffY = (data[i][header[y]] - data[i-1][header[y]]) / time_step

            velocity = sqrt(diffX ** 2 + diffY ** 2) 
            derived[i][derive_header["Velocity"+c[0]]] = velocity

def calculate_angular_v(derived, data):

    for i in range(1, len(data)):
        
        for c in colours:
            armx1, army1 = get_arm(data[i-1], c)
            dist1, angle1 = polar(armx1, army1)
            armx2, army2 = get_arm(data[i], c)
            dist2, angle2 = polar(armx2, army2)

            angular_vel = (angle2 - angle1) / time_step
            derived[i][derive_header["Angular"+c[0]]] = angular_vel

def calculate_cm(derived, data):
    for i in range(len(data)):
        for c in colours:
            root_colour = get_root_colour(c)
            
            rootx = data[i][header[root_colour+"X"]]
            rooty = data[i][header[root_colour+"Y"]]
            armx, army = get_arm(data[i], c)

            cmx = rootx
            cmy = rooty
            if c == "Yellow":
                cmx += armx * cm_yellow
                cmy += army * cm_yellow
            if c == "Pink":
                cmx += armx * cm_pink
                cmy += army * cm_pink
            if c == "Green":
                cmx += armx * cm_green
                cmy += army * cm_green
                
            derived[i][derive_header["Center"+c[0]+"x"]] = cmx
            derived[i][derive_header["Center"+c[0]+"y"]] = cmy

            
def get_potential(y, colour):
    zero = 0
    mass = 0
    if colour == "Yellow":
        zero = -length * cm_yellow
        mass =  m_yellow + m_arm
    if colour == "Pink":
        zero = -length + (-length * cm_pink)
        mass =  m_pink + m_arm
    if colour == "Green":
        zero = -2*length + (-length * cm_green)
        mass =  m_green + m_arm

    displacement = y - zero
    return displacement * mass * 9.81
        

def calculate_translational(derived):
    for i in range(len(derived)):
        
        energy = (derived[i][derive_header["VelocityY"]] ** 2)  * 0.5 * m_yellow
        derived[i][derive_header["TransY"]] = energy
        energy = (derived[i][derive_header["VelocityP"]] ** 2)  * 0.5 * m_pink
        derived[i][derive_header["TransP"]] = energy
        energy = (derived[i][derive_header["VelocityG"]] ** 2)  * 0.5 * m_green
        derived[i][derive_header["TransG"]] = energy

def calculate_rotational(derived):
    for i in range(len(derived)):

        I_yellow = (1/12) * m_arm * (arm_length ** 2)
        I_pink = (1/12) * m_arm * (arm_length ** 2)
        I_green = (1/12) * m_arm * (arm_length ** 2)
        
        energy = ((derived[i][derive_header["AngularY"]] * (pi/180)) ** 2)  * 0.5 * I_yellow
        derived[i][derive_header["RotateY"]] = energy
        energy = ((derived[i][derive_header["AngularP"]] * (pi/180)) ** 2)  * 0.5 * I_pink
        derived[i][derive_header["RotateP"]] = energy
        energy = ((derived[i][derive_header["AngularG"]] * (pi/180)) ** 2)  * 0.5 * I_green
        derived[i][derive_header["RotateG"]] = energy
    

def calculate_translational(derived):
    for i in range(len(derived)):
        
        energy = (derived[i][derive_header["VelocityY"]] ** 2)  * 0.5 * m_yellow
        derived[i][derive_header["TransY"]] = energy
        energy = (derived[i][derive_header["VelocityP"]] ** 2)  * 0.5 * m_pink
        derived[i][derive_header["TransP"]] = energy
        energy = (derived[i][derive_header["VelocityG"]] ** 2)  * 0.5 * m_green
        derived[i][derive_header["TransG"]] = energy

def calculate_potential(derived):
    for i in range(len(derived)):
        
        derived[i][derive_header["EnergyY"]] = get_potential(derived[i][derive_header["CenterYy"]], "Yellow")
        derived[i][derive_header["EnergyP"]] = get_potential(derived[i][derive_header["CenterPy"]], "Pink")
        derived[i][derive_header["EnergyG"]] = get_potential(derived[i][derive_header["CenterGy"]], "Green")


def calculate_total(derived):
    for i in range(len(derived)):

        for c in colours:

            trans = derived[i][derive_header["Trans"+c[0]]]
            rot = derived[i][derive_header["Rotate"+c[0]]]
            pot = derived[i][derive_header["Energy"+c[0]]]

            derived[i][derive_header["Total" + c[0]]] = trans + rot + pot
            derived[i][derive_header["TotalEnergy"]] += trans + rot + pot

def write_csv(derived, data):
    
    f = open(write_to, "w")
    
    header_line = ""
    for h in derive_keys:
        header_line += h + ","
    header_line.strip(",")
    f.write(header_line + "\n")
    
    for i in range(len(derived)):
        if data[i][header["Time"]] < 10 or data[i][header["Time"]] > 40:
            continue

        line = ""
        line += str(data[i][header["Recording"]]) + ","
        line += str(i) + ","
        line += str(data[i][header["Time"]]) + ","
         
        for d in derived[i][3:]:
            line += str(d) + ","
        line.strip(",")

        f.write(line + "\n")
    
    f.close()

f = open(read_from, "r")
lines = f.readlines()

top = lines[0].split(',')
count = 0
for t in top:
    header[t] = count
    count += 1

lines = lines[1:]
data = []
for l in lines:
    l = l.split(',')

    if l[2] != "prop":
        continue

    for h in header.values():
        if h == header["Type"]:
            continue
        l[h] = float(l[h])
    
    data.append(l)


derived = []
for n in data:
    row = []
    for x in derive_keys:
        row.append(0.0)
    derived.append(row)

calculate_velocity(derived, data)
calculate_angular_v(derived, data)
calculate_cm(derived, data)
calculate_translational(derived)
calculate_rotational(derived)
calculate_potential(derived)
calculate_total(derived)

write_csv(derived, data)