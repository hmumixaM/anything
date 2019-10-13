import numpy as np
import math as m
import matplotlib.pyplot as plt

def minimize(angle):
    while angle >= 2 * m.pi:
        angle -= 2 * m.pi
    return angle


def move(x, y, angle):
    x += m.cos(angle)
    y += m.sin(angle)
    return x, y


def sel(listt, index):
    temp = []
    for i in listt:
        temp.append(i[index])
    return temp


def location(ratio, num_points):
    angle_diff = 2 * m.pi / (ratio + 1)
    position = []
    for _ in range(num_points):
        angle = minimize(angle_diff * _)
        x, y = move(0, 0, angle)
        position.append([x, y, angle])
        for i in range(len(position)):
            x, y, angle = position[i][0], position[i][1], position[i][2]
            position[i][0], position[i][1] = move(x, y, angle)
    return position


if __name__ == "__main__":
	ratio = float(input("Input the ratio you want: "))
	points = int(input("Input the number of points you want: "))
	fig, ax = plt.subplots(num=1, clear=True)
	
	position = location(ratio, points)
	xs = sel(position, 0)
	ys = sel(position, 1)

	ax.plot(xs, ys, 'g.')
	ax.grid(True)
	ax.axis("equal")
	fig.tight_layout()

	fig.savefig('hw.png')
	print("Finished! Go hw.png to see the result.")
