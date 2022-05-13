
import numpy as np
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

x_fuse =[0]
y_fuse = [0]
alph = 0.25
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
plt.title("GPS Positioning Fuse 0.075 Alpha")
plt.xlabel("X axis (m)")
plt.ylabel("Y axis (m)")
plt.savefig("gps_plot_fuse_upd_0.075.png")


