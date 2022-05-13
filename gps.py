import numpy as np
import matplotlib.pyplot as plt


f = open("positionObs_cleaned.txt", "r")
f_read = f.read()
f_split1 = f_read.split("\n")
time_s_gps = []
time_ms_gps = []
x_gps = []
y_gps = []

for data in f_split1:
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

print(len(x_gps))
print(len(y_gps))

plt.grid()
plt.plot(x_gps, y_gps)
plt.title("GPS Positioning")
plt.xlabel("X axis (m)")
plt.ylabel("Y axis (m)")
plt.savefig("gps_plot.png")