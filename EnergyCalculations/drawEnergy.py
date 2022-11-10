import matplotlib.pyplot as plt
from scipy import stats

read_from = "./energyData.csv"
save_path = "./graphs/"

run_data = {"223": [], "224": [], "225": [], "226": [], "227":[], "228":[], "229":[], "230":[], "231":[], "233":[], "234":[], "235":[]}

energy_trials = {"45": ["223", "224", "225"], "90":["226", "227", "228"], "135":["229", "230", "231"], "180":["233", "234", "235"]}

energy_stats = {}
for t in energy_trials.keys():
    energy_stats[t] = [0, 0, 0]

run_stats = {}
for r in run_data.keys():
    run_stats[r] = {}
    

header = {}
header_keys = ["Run","Frame","Time",
                  "VelocityY",	"VelocityP", "VelocityG",
                  "AngularY", "AngularP", "AngularG",
                  "CenterYx", "CenterYy", "CenterPx", "CenterPy", "CenterGx", "CenterGy",
                  "TransY", "TransP", "TransG", 
                  "RotateY", "RotateP", "RotateG",
                  "EnergyY", "EnergyP", "EnergyG",
                  "TotalY", "TotalP", "TotalG",
                  "TotalEnergy"]

for i in range(len(header_keys)):
    header[header_keys[i]] = i


colours = ["Yellow", "Pink", "Green"]
all_colours = ["Blue", "Yellow", "Pink", "Green"]
time_step = 0.008333

def get_run(data, run, head):
    x_data = []
    y_data = []
    for d in data:
        if d[header["Run"]] == run:
            x_data.append(d[header["Time"]])
            y_data.append(d[header[head]])

    return (x_data, y_data)

def calc_stats(data, run_stats):

    for r in run_data.keys():
        for c in colours:
            x, y = get_run(data, r, "Total"+c[0])

            slope, intercept, re, p, std_err = stats.linregress(x, y)
            print(r, c, slope, intercept, std_err, sep=",")
            run_stats[r]["Total"+c[0]] = (slope, intercept, std_err)

        x, y = get_run(data, r, "TotalEnergy")

        slope, intercept, re, p, std_err = stats.linregress(x, y)
        print(r, "TotalEnergies", slope, intercept, std_err, sep=",")
        run_stats[r]["TotalEnergy"] = (slope, intercept, std_err)

            

def remove_outliers(data, run_stats):

    tolerance = 0.4
    
    for i in range(len(data)):
        point = data[i]
        data[i][header["TotalEnergy"]] =  0
           
        for c in colours:
            point_total = point[header["Total"+c[0]]]
            time = point[header["Time"]]
            slope, intercept, std_err = run_stats[point[header["Run"]]]["Total"+c[0]]

            diff = abs(point_total - (intercept + slope * time))
            #print(diff, std_err * 2, diff > tolerance)
            if diff > tolerance:
                data[i][header["Total"+c[0]]] = 0

            data[i][header["TotalEnergy"]] += data[i][header["Total"+c[0]]]


def draw_variable(data, var):
    x, y = get_run(data, "227", var)
    plt.figure(1)
    plt.plot(x, y)
    plt.suptitle(var)
    plt.show()

def draw_gravitational(data, var):
    x, y_cm = get_run(data, "223", "Center" + var[0] + "y")
    x, y_grav = get_run(data, "223", "Energy" + var[0])
    plt.plot(x, y_cm, "blue", x, y_grav, "black")
    plt.suptitle(var + " Gravitational")
    plt.show()


def draw_totalEnergies(data, run, fig):
    plt.figure(fig)

    x, y_y = get_run(data, run, "TotalY")
    x, y_p = get_run(data, run, "TotalP")
    x, y_g = get_run(data, run, "TotalG")
    x, y = get_run(data, run, "TotalEnergy")

    plt.plot(x, y_y, "yellow", label="Yellow")
    plt.plot(x, y_p, "red", label="Pink")
    plt.plot(x, y_g, "green", label="Green")
    plt.plot(x,y, "black", label="Total", linestyle="--")

    plt.xlim([10, 40])
    plt.legend(loc="upper left")
    plt.xlabel("Time (sec)")
    plt.ylabel("Energy (J)")
    title = "Run " + run + ": Total energy of each arm"
    plt.suptitle(title)
    plt.savefig(save_path+title)
    plt.show()

def draw_allEnergy(data, colour, run, fig):
    plt.figure(fig)
    
    x, y_tran = get_run(data, run, "Trans"+colour[0])
    x, y_rot = get_run(data, run, "Rotate"+colour[0])
    x, y_pot = get_run(data, run, "Energy"+colour[0])
    x, y_tot = get_run(data, run, "Total"+colour[0])

    plt.plot(x, y_tran, "blue", label="Translational")
    plt.plot(x, y_rot, "green", label="Rotational")
    plt.plot(x, y_pot, "red", label = "Gravitational")
    plt.xlim([20, 40])

    title = "Run " + run + ": energy of " + colour.lower() + " breakdown"
    plt.suptitle(title)
    plt.legend(loc="upper left")
    plt.xlabel("Time (sec)")
    plt.ylabel("Energy (J)")
    plt.savefig(save_path+title)
    plt.show()

def draw_stats_energies(data, run_stats, run, fig):

    plt.figure(fig)
    run_stat = run_stats[run]
    x, y = get_run(data, run, "TotalEnergy")

    y_yellow = [run_stat["TotalY"][1] + run_stat["TotalY"][0] * t for t in x]
    y_pink = [run_stat["TotalP"][1] + run_stat["TotalP"][0] * t for t in x]
    y_green = [run_stat["TotalG"][1] + run_stat["TotalG"][0] * t for t in x]
    y_total = [run_stat["TotalEnergy"][1] + run_stat["TotalEnergy"][0] * t for t in x]
    

    plt.plot(x, y_yellow, "yellow", label='Yellow')
    plt.plot(x, y_pink, "red", label='Pink')
    plt.plot(x, y_green, "green", label='Green')
    plt.plot(x, y_total, "black", label='Total', linestyle="--")

    title = "Run " + run +": average of total energy of each arm"
    plt.legend(loc="upper left")
    plt.xlabel("Time (sec)")
    plt.ylabel("Average Energy (J)")
    plt.suptitle(title)
    plt.savefig(save_path + title)
    plt.show()


f = open(read_from, "r")
lines = f.readlines()

lines = lines[1:]
data = []
for l in lines:
    l = l.strip("\n").split(',')

    for i in range(len(header_keys)):
        if header_keys[i] != "Run":
            try:
                l[i] = float(l[i])
            except Exception:
                l[i] = 0
        else:
            l[i] = str(int(float(l[i])))
    
    data.append(l)

run = "223"
calc_stats(data, run_stats)
remove_outliers(data, run_stats)
calc_stats(data, run_stats)

draw_allEnergy(data, "Yellow", run, 1)
draw_allEnergy(data, "Pink", run, 2)
draw_allEnergy(data, "Green", run, 3)
draw_totalEnergies(data, run, 4)
draw_stats_energies(data, run_stats, run, 5)
