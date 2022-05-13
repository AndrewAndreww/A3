### import the modules and packages needed

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

### plot the graph
plt.grid()
plt.plot(xData, yData)
plt.title("Dead Reckoning Positioning")
plt.xlabel("X axis (m)")
plt.ylabel("Y axis (m)")
plt.savefig("dead_reckoning.png")

### animate the graph into .gif format
fig, ax = plt.subplots()
ax.grid()
print(plt.subplots())
ax.set_title("Dead Reckoning Positioning")
ax.set_xlabel("X position (m)")
ax.set_ylabel("Y position (m)")

ax.set_xlim(min(xData), max(xData))
ax.set_ylim(min(yData), max(yData))

line, = ax.plot([], [])

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = xData[:i + 1]
    y = yData[:i + 1]
    line.set_data(x, y)  # plot each x point and ypoint at each frame
    return line,

anim = FuncAnimation(fig, animate, init_func=init, frames=len(xData), interval=0.01)
anim.save('animation.gif')
