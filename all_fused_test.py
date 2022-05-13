import numpy as np
import math
import matplotlib.pyplot as plt


### open and read the cleaned txt file, then split for each new line
f = open("velocityObs_cleaned.txt", "r")
f_read = f.read()
f_split1 = f_read.split("\n")
time_s = []
time_ms = []
vel = []
turn_rate = []
time = []


### using for loop, loop through each line and split if there is a space.
### the splitted values will then be appended into different variables.
for data in f_split1:
    time_s.append(int(data.split(" ")[0]))
    time_ms.append(float(data.split(" ")[1]))
    vel.append(float(data.split(" ")[2]))
    turn_rate.append(float(data.split(" ")[3]))

### convert the lists into arrays to make mathematical operations simpler.
arr_time_s = np.array(time_s)
arr_time_ms = np.array(time_ms) * (10 ** (-6))
arr_vel = np.array(vel)
arr_turn_rate = np.array(turn_rate)
arr_time = arr_time_s + arr_time_ms
arr_time = arr_time - arr_time_s[0]

### finding delta time using numpy arrays
time = arr_time.tolist()
time.insert(0, 0.0)
del time[-1]
arr_time_new = np.array(time)
delta_time = arr_time - arr_time_new

### convert turn rates into headings
arr_heading = arr_turn_rate * delta_time
heading_list = arr_heading.tolist()


### define a function to calculate cumulative sum
def nums_cumulative_sum(nums_list):
    return [sum(nums_list[:i + 1]) for i in range(len(nums_list))]

headingData = nums_cumulative_sum(heading_list)

### calculate the sine and cosine of heading of the robot
headingData = np.array(headingData)
headingData_list = headingData.tolist()
headingData_cos = np.cos(headingData)
headingData_sin = np.sin(headingData)
headingData_cos_list = headingData_cos.tolist()
headingData_sin_list = headingData_sin.tolist()

### calculate the distance traveled in x and y coordinates
x = delta_time * arr_vel * headingData_cos
x_list = x.tolist()

y = delta_time * arr_vel * headingData_sin
y_list = y.tolist()

xData = nums_cumulative_sum(x_list)
yData = nums_cumulative_sum(y_list)


###GPS
g = open("positionObs_cleaned.txt", "r")
g_read = g.read()
g_split1 = g_read.split("\n")
time_s_gps = []
time_ms_gps = []
x_gps = []
y_gps = []

for data in g_split1:
    time_s_gps.append(int(data.split()[0]))
    time_ms_gps.append(float(data.split()[1]))
    x_gps.append(float(data.split()[2]))
    y_gps.append(float(data.split()[3]))

arr_time_s_gps = np.array(time_s_gps)
arr_time_ms_gps = np.array(time_ms_gps) * 10 ** (-6)
arr_x_gps = np.array(x_gps)
arr_y_gps = np.array(y_gps)
arr_time_gps = arr_time_s_gps + arr_time_ms_gps
arr_time_gps = arr_time_gps - arr_time_s_gps[0]
time_gps = arr_time_gps.tolist()
time_gps.insert(0, 0.0)
del time_gps[-1]
arr_time_new_gps = np.array(time_gps)
delta_time_gps = arr_time_gps - arr_time_new_gps


###compass
h = open("compassObs_cleaned.txt", "r")
h_read = h.read()
h_split1 = h_read.split("\n")
time_s_compass = []
time_ms_compass = []
heading_compass = []

for data in h_split1:
    time_s_compass.append(int(data.split()[0]))
    time_ms_compass.append(float(data.split()[1]))
    heading_compass.append(float(data.split()[2]))

arr_time_s_compass = np.array(time_s_compass)
arr_time_ms_compass = np.array(time_ms_compass) * 10 ** (-6)
arr_heading_compass = np.array(heading_compass)
arr_time_compass = arr_time_s_compass + arr_time_ms_compass
arr_time_compass = arr_time_compass - arr_time_s_compass[0]
time_compass = arr_time_compass.tolist()
time_compass.insert(0, 0.0)
del time_compass[-1]
arr_time_new_compass = np.array(time_compass)
delta_time_compass = arr_time_compass - arr_time_new_compass


heading_compass_upd = []
for heading in heading_compass:
    if heading < 0:
        heading = heading + 2 * math.pi
        heading_compass_upd.append(heading)
    else:
        heading_compass_upd.append(heading)

###debug1
heading_compass_upd_mod = []
for heading in heading_compass_upd:
    heading = heading % (2 * math.pi)
    heading_compass_upd_mod.append(heading)


###change the heading into cartesian form
heading_compass_cart =[]
for heading in heading_compass_upd_mod:
    heading = (heading - (0.5 * math.pi)) * (-1)
    heading = heading % (2 * math.pi)
    heading_compass_cart.append(heading)


### change the heading into positive angles
# print(heading_compass_cart)
heading_compass_cart_upd = []
for heading in heading_compass_cart:
    if heading < 0:
        heading = heading + (2 * math.pi)
        heading_compass_cart_upd.append(heading)
    else:
        heading_compass_cart_upd.append(heading)


### account for angular wraps
headingData_list_upd = []
for heading in headingData_list:
    if heading > 2*math.pi:
        heading = heading % (2 * math.pi)
        headingData_list_upd.append(heading)
    elif heading < 2*math.pi:
        heading = heading % (-2 * math.pi)
        headingData_list_upd.append(heading)
    else:
        headingData_list_upd.append(heading)
# print(headingData_list_upd)

###change the heading into positive angles
headingData_list_equi = []
for heading in headingData_list_upd:
    if heading < 0:
        heading = heading + (2 * math.pi)
        headingData_list_equi.append(heading)
    else:
        headingData_list_equi.append(heading)


###Fuse (?)

if time in time_compass:
    print("aaaaaaaa")

x_fuse = [0]
y_fuse = [0]
heading_fuse = [0.0]
alph_gps = 0.1
alph_compass = 0.0025
k = 0
p = 0
for i in range(len(xData)-1):
    if time[i] in time_gps:

        x = x_fuse[i] + alph_gps * (x_gps[k]-x_fuse[i])
        x_fuse.append(x)

        y = y_fuse[i] + alph_gps * (y_gps[k] - y_fuse[i])
        y_fuse.append(y)

        heading = heading_fuse[i] + delta_time[i] * turn_rate[i]
        heading_fuse.append(heading)

        k = k + 1
    elif time[i] in time_compass:
        diff = heading_compass_cart_upd[p] - headingData_list_equi[i]
        ### account for angular wraps
        if ((0 < headingData_list_equi[i] < 0.5 * math.pi) and (2*math.pi < heading_compass_cart_upd[p] < 1.5 * math.pi)):
            diff = (heading_compass_cart_upd[p] - (2 * math.pi)) - headingData_list_equi[i]
        elif ((0 < heading_compass_cart_upd[p] < 0.5 * math.pi) and (2*math.pi < headingData_list_equi[i] < 1.5 * math.pi)):
            diff = (headingData_list_equi[i] - (2 * math.pi)) - heading_compass_cart_upd[p]
        elif ((0.5 * math.pi < headingData_list_equi[i] < math.pi) and (2*math.pi < heading_compass_cart_upd[p] < 1.5 * math.pi)) and diff > math.pi:
            diff = diff - 2 * math.pi
        elif ((0.5 * math.pi < heading_compass_cart_upd[p] < math.pi) and (2*math.pi < headingData_list_equi[i] < 1.5 * math.pi)) and diff < math.pi:
            diff = diff + 2 * math.pi
        elif ((0.5 * math.pi < heading_compass_cart_upd[p] < 0) and (1.5*math.pi < headingData_list_equi[i] < math.pi)) and diff < math.pi:
            diff = diff + 2* math.pi
        elif ((0.5 * math.pi < headingData_list_equi[i] < 0) and (1.5*math.pi < heading_compass_cart_upd[p] < math.pi)) and diff > math.pi:
            diff = diff - 2*math.pi
        else:
            diff = diff


        heading = heading_fuse[i] + delta_time[i] * turn_rate[i] + (alph_compass * diff)
        heading_fuse.append(heading)
        p = p+1

        x = x_fuse[i] + delta_time[i] * vel[i] * heading_fuse[i]
        x_fuse.append(x)
        y = y_fuse[i] + delta_time[i] * vel[i] * heading_fuse[i]
        y_fuse.append(y)
    else:
        heading = heading_fuse[i] + delta_time[i] * turn_rate[i]
        heading_fuse.append(heading)
        x = x_fuse[i] + delta_time[i] * vel[i] * math.cos(heading_fuse[i])
        x_fuse.append(x)
        y = y_fuse[i] + delta_time[i] * vel[i] * math.sin(heading_fuse[i])
        y_fuse.append(y)


plt.grid()
plt.plot(x_fuse, y_fuse)
plt.title("GPS 0.1 and Compass 0.0025")
plt.xlabel("X axis (m)")
plt.ylabel("Y axis (m)")
plt.savefig("fusion_0.1_0.0025.png")


###laser features

g = open("laserFeatures_cleaned.txt", "r")
g_read = g.read()
g_split1 = g_read.split("\n")
x_laser = []
y_laser = []

for data in g_split1:
    x_laser.append(float(data.split()[0]))
    y_laser.append(float(data.split()[1]))

plt.grid()
plt.scatter(x_laser, y_laser, facecolors='none', edgecolors='r', s=75)
plt.title("Laser Features Positions")
plt.xlabel("X axis (m)")
plt.ylabel("Y axis (m)")
# plt.savefig("fusion_0.0.png")


### laserObs

f = open("laserObs_cleaned.txt", "r")
f_read = f.read()
f_split1 = f_read.split("\n")
time_s_laser = []
time_ms_laser = []
range_intensity = []
laser_range = []
laser_intensity = []

for data in f_split1:
    data_split = data.split()
    time_s_laser.append(float(data_split[0]))
    time_ms_laser.append(float(data_split[1]))
    laser_range.append(data_split[2::2])
    laser_intensity.append(data_split[3::2])

arr_time_s_laser = np.array(time_s_laser)
arr_time_ms_laser = np.array(time_ms_laser) * 10 ** (-6)
arr_time_laser = arr_time_s_laser + arr_time_ms_laser
arr_time_laser = arr_time_laser - arr_time_s_laser[0]
time_laser = arr_time_laser.tolist()

# delta_time_dr_laser = arr_time - arr_time_laser

laser_range_num = [[float(ele) for ele in sub] for sub in laser_range]

print(len(laser_range_num[2835]))
print(laser_range_num[2835])

ls = []
for i in range(600):
    ls1 = []
    for j in range(600):
        ls1.append(0)
    ls.append(ls1)

# print(time_laser)
# print(len(x_fuse))
x_obstacle = []
y_obstacle = []
#
for i in range(len(time_laser)-1):
    # print(i)
    a = laser_range_num[i]
    for j in range(len(a)):
        if laser_range_num[i][j] != 8:
            psi = heading_fuse[i+3] + ((-0.5 * math.pi) + (j * 0.5 * math.pi/180))
            if psi > 0:
                psi = psi % (2*math.pi)
            else:
                psi = psi % (-2*math.pi)

            if psi > math.pi:
                psi = psi - (2 * math.pi)
            elif psi < -math.pi:
                psi = psi + (2 * math.pi)
            else:
                psi = psi
            x = round(x_fuse[i+3] + laser_range_num[i][j] * math.cos(psi),2)
            x = (x/0.1)
            x = round(x + 300)
            x_obstacle.append(x)
            y = round(y_fuse[i+3] + laser_range_num[i][j] * math.sin(psi),2)
            y = (y/0.1)
            y = round(y + 300)
            y_obstacle.append(y)
        else:
            pass

# print(x_obstacle[1])
# print(y_obstacle[1])

for i in range(len(x_obstacle)):
    ls[599 - y_obstacle[i]][x_obstacle[i]] = ls[599 - y_obstacle[i]][x_obstacle[i]] + 1


print(ls)

threshold = 40

for i in range(len(ls)):
    for j in range(len(ls[0])):
        if ls[i][j]<threshold:
            ls[i][j] = 0
        else:
            ls[i][j] = 1


import csv
f = open("gpscompass_fuse_0.25_0.0005_res600t40.txt", "w")

writer = csv.writer(f)
writer.writerows(ls)
f.close()

