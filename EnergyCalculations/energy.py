
from math import sqrt


read_from = "../allData.csv"
write_to = "./energData.csv"
header = {}
derive_header = {}

colours = ["Yellow", "Pink", "Green"]

def calculate_velocity(derived, data):

    for i in range(1, len(data)):
        
        for c in colours:
            x = c+"X"
            y = c+"Y"
            diffX = data[i][header[x]] - data[i-1][header[x]]
            diffY = data[i][header[y]] - data[i-1][header[y]]

            velocity = sqrt(diffX ** 2 + diffY ** 2)
            print(velocity)
        

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

    for h in header.values():
        if h == header["Type"]:
            continue
        l[h] = float(l[h])
    
    data.append(l)

derive_header = {"Frame": 0, "Time": 1,
                 "VelocityY" : 2, "VelocityP": 3, "VeloctiyG": 4,
                 "AngularY": 5, "AngularP" : 6, "AngularG": 7,
                 "CenterY":8, "CenterP" : 9, "CenterG": 10,
                 "TransY": 11, "TransP": 12, "TransG": 13,
                 "RotateY" : 14, "RotateP" : 15, "RotateG" : 16,
                 "EnergyY" : 17, "EnergyP" : 18, "EnergyG" : 19,
                 "TotalEnergy": 20} 

derived = []

data = data[:100]
calculate_velocity(derived, data)
