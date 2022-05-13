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
# print(headingData)

headingData = np.array(headingData)
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


###GPS data

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

###Fuse (?)

x_fuse =[0]
y_fuse = [0]
alph = 0.075
k = 0
for i in range(len(xData)-1):
    if time[i] in time_gps:
        x = x_fuse[i] + alph*(x_gps[k]-x_fuse[i])
        x_fuse.append(x)
        k = k+1
    else:
        x = x_fuse[i] + delta_time[i]*vel[i]*headingData_cos_list[i]
        x_fuse.append(x)
p = 0
for i in range(len(xData)-1):
    if time[i] in time_gps:
        y = y_fuse[i] + alph*(y_gps[p]-y_fuse[i])
        y_fuse.append(y)
        p = p+1
    else:
        y = y_fuse[i] + delta_time[i]*vel[i]*headingData_sin_list[i]
        y_fuse.append(y)


plt.grid()
plt.plot(x_fuse, y_fuse)
plt.title("GPS Positioning Fuse 0.9 Alpha")
plt.xlabel("X axis (m)")
plt.ylabel("Y axis (m)")
# plt.savefig("gps_plot_fuse_upd.png")

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
# plt.savefig("laser_features_!!_gps.png")

### laserObs

m = open("laserObs_cleaned.txt", "r")
m_read = m.read()
m_split1 = m_read.split("\n")
time_s_laser = []
time_ms_laser = []
range_intensity = []
laser_range = []
laser_intensity = []

for data in m_split1:
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

laser_range_num = [[float(ele) for ele in sub] for sub in laser_range]

###occupancy grid of 600 x 600 resolution
ls = []
for i in range(600):
    ls1 = []
    for j in range(600):
        ls1.append(0)
    ls.append(ls1)

x_obstacle = []
y_obstacle = []

for i in range(len(time_laser)-1):

    a = laser_range_num[i]
    for j in range(len(a)):
        if laser_range_num[i][j] < 8:

            psi = headingData[i+3] + ((-0.5 * math.pi) + (j * 0.5 * (math.pi/180)))
            if psi > 0:
                psi = psi % (2*math.pi)
            else:
                psi = psi % (-2*math.pi)

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

            x = round(x_fuse[i+3] + (laser_range_num[i][j] * math.cos(psi)), 2)
            x = (x/(1/15))
            x = int(round(x + 300))
            x_obstacle.append(x)
            y = round(y_fuse[i+3] + (laser_range_num[i][j] * math.sin(psi)), 2)
            y = (y/(1/15))
            y = int(round(y + 300))
            y_obstacle.append(y)
        else:
            pass


for i in range(len(x_obstacle)):
    ls[599 - y_obstacle[i]][x_obstacle[i]] = ls[599 - y_obstacle[i]][x_obstacle[i]] + 1

#threshold value of 50
threshold = 50

for i in range(len(ls)):
    for j in range(len(ls[0])):
        if ls[i][j]<threshold:
            ls[i][j] = 0
        else:
            ls[i][j] = 1


import csv
f = open("gpsfuse_res600t50.txt", "w")

writer = csv.writer(f)
writer.writerows(ls)
f.close()
