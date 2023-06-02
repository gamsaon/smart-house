from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random

def update_plot(x, y, z):
    xdata.append(x)  # x 좌표 추가
    ydata.append(y)
    zdata.append(z)  # y 좌표 추가
    #=ln.set_data(xdata, ydata, zdata)  # 점 좌표 업데이트
    ax.scatter(xdata, ydata, zdata, c='black', marker='o', s=1, cmap='Greens')
    ax.relim()  # 축 범위 재설정


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xdata, ydata, zdata = [], [], []

ax.set_xlim3d(0,100)
ax.set_ylim3d(0,100)
ax.set_zlim3d(0,100)
h1, = ax.plot3D([],[],[])
i=0
while 1:
    i = i+1
    if i>100:
        break
    x = random.randint(0,100)
    y = random.randint(0,100)
    z = random.randint(0,100) 
    update_plot(x, y, z)
    plt.pause(0.1)

plt.show()
