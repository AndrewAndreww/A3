import numpy as np
import math
import matplotlib.pyplot as plt


###Dead Reckoning Data

f = open("velocityObs_cleaned.txt", "r")
f_read = f.read()
f_split1 = f_read.split("\n")
time_s = []
time_ms = []
vel = []
turn_rate = []
time = []

for data in f_split1:
    time_s.append(int(data.split(" ")[0]))
    time_ms.append(float(data.split(" ")[1]))
    vel.append(float(data.split(" ")[2]))
    turn_rate.append(float(data.split(" ")[3]))

arr_time_s = np.array(time_s)
arr_time_ms = np.array(time_ms) * 10 ** (-6)
arr_vel = np.array(vel)
arr_turn_rate = np.array(turn_rate)
arr_time = arr_time_s + arr_time_ms
arr_time = arr_time - arr_time_s[0]
time = arr_time.tolist()
time.insert(0, 0.0)
del time[-1]
arr_time_new = np.array(time)
delta_time = arr_time - arr_time_new

arr_heading = arr_turn_rate * delta_time
heading_list = arr_heading.tolist()

def nums_cumulative_sum(nums_list):
    return [sum(nums_list[:i + 1]) for i in range(len(nums_list))]

headingData = nums_cumulative_sum(heading_list)

headingData = np.array(headingData)
headingData_list = headingData.tolist()
headingData_cos = np.cos(headingData)
headingData_sin = np.sin(headingData)
headingData_cos_list = headingData_cos.tolist()
headingData_sin_list = headingData_sin.tolist()

x = delta_time * arr_vel * headingData_cos
x_list = x.tolist()

y = delta_time * arr_vel * headingData_sin
y_list = y.tolist()

xData = nums_cumulative_sum(x_list)
yData = nums_cumulative_sum(y_list)


###Compass data

g = open("compassObs_cleaned.txt", "r")
g_read = g.read()
g_split1 = g_read.split("\n")
time_s_compass = []
time_ms_compass = []
heading_compass = []

for data in g_split1:
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

###Fuse (?)

heading_compass_upd = []
for heading in heading_compass:
    if heading < 0:
        heading = heading + 2 * math.pi
        heading_compass_upd.append(heading)
    else:
        heading_compass_upd.append(heading)


###change the heading into cartesian form
heading_compass_cart =[]
for heading in heading_compass_upd:
    heading = (heading - (0.5 * math.pi)) * (-1)
    heading_compass_cart.append(heading)


### change the heading into positive angles

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


###change the heading into positive angles
headingData_list_equi = []
for heading in headingData_list_upd:
    if heading < 0:
        heading = heading + (2 * math.pi)
        headingData_list_equi.append(heading)
    else:
        headingData_list_equi.append(heading)


x_fuse = [0]
y_fuse = [0]
heading_fuse =[0.0]
alph = 0.1
k = 0
len_diff =[]
aaa = []
bbb = []
ccc = []
for i in range(len(xData)-1):
    if time[i] in time_compass:
        diff = heading_compass_cart_upd[k] - headingData_list_equi[i]
        if ((0 < headingData_list_equi[i] < 0.5 * math.pi) and (2*math.pi < heading_compass_cart_upd[k] < 1.5 * math.pi)):
            diff = (heading_compass_cart_upd[k] - (2 * math.pi)) - headingData_list_equi[i]
        elif ((0 < heading_compass_cart_upd[k] < 0.5 * math.pi) and (2*math.pi < headingData_list_equi[i] < 1.5 * math.pi)):
            diff = (headingData_list_equi[i] - (2 * math.pi)) - heading_compass_cart_upd[k]
        elif ((0.5 * math.pi < headingData_list_equi[i] < math.pi) and (2*math.pi < heading_compass_cart_upd[k] < 1.5 * math.pi)) and diff > math.pi:
            diff = diff - 2 * math.pi
        elif ((0.5 * math.pi < heading_compass_cart_upd[k] < math.pi) and (2*math.pi < headingData_list_equi[i] < 1.5 * math.pi)) and diff < math.pi:
            diff = diff + 2 * math.pi
        elif ((0.5 * math.pi < heading_compass_cart_upd[k] < 0) and (1.5*math.pi < headingData_list_equi[i] < math.pi)) and diff < math.pi:
            diff = diff + 2* math.pi
        elif ((0.5 * math.pi < headingData_list_equi[i] < 0) and (1.5*math.pi < heading_compass_cart_upd[k] < math.pi)) and diff > math.pi:
            diff = diff - 2*math.pi
        else:
            diff = diff
        ### account for angular wraps
        if diff > math.pi:
            diff = diff - (2 * math.pi)
        elif diff < -math.pi:
            diff = diff + (2 * math.pi)
        else:
            diff = diff

        heading = heading_fuse[i] + delta_time[i]*turn_rate[i] + alph * diff
        heading_fuse.append(heading)
        k = k+1
    else:
        heading = heading_fuse[i] + delta_time[i]*turn_rate[i]
        heading_fuse.append(heading)


arr_heading_fuse = np.array(heading_fuse)
arr_heading_fuse_cos = np.cos(heading_fuse)
arr_heading_fuse_sin = np.sin(heading_fuse)
heading_fuse_cos_list = arr_heading_fuse_cos.tolist()
heading_fuse_sin_list = arr_heading_fuse_sin.tolist()

x_compass = delta_time * arr_vel * arr_heading_fuse_cos
x_compass_list = x_compass.tolist()

y_compass = delta_time * arr_vel * arr_heading_fuse_sin
y_compass_list = y_compass.tolist()

xData_fuse = nums_cumulative_sum(x_compass_list)
yData_fuse = nums_cumulative_sum(y_compass_list)

plt.grid()
plt.plot(xData_fuse, yData_fuse)
plt.title("Dead Reckoning Positioning Fuse Compass 0.1")
plt.xlabel("X axis (m)")
plt.ylabel("Y axis (m)")
plt.savefig("compass_fuse.png")