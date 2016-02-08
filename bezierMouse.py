import numpy as np
import matplotlib.pyplot as plt
from pymouse import PyMouse
from time import sleep
from random import randint as random

def linear_bezier(point1, point2, t):
    return (1.0 - t) * point1 + t * point2

def interpolate_control_points(points, t):
    return [
        linear_bezier(point1, point2, t)
        for point1, point2 in zip(points, points[1:])]

def bezier(control_points, t, stoplevel=2):
    points = points_as_arrays(control_points)
    while len(points) > stoplevel:
        points = interpolate_control_points(points, t)
    return linear_bezier(points[0], points[1], t)

def points_as_arrays(point_tuples):
    return [np.array(point) for point in point_tuples]

NPTS = 100

p0 = (random(0,1440), random(0,200))
p1 = (random(0,1440), random(700,900))

pxdiff = p1[0] - p0[0]
pydiff = p1[1] - p0[1]

control_points = [p0, (p0[0]/1.5,p0[0]/1.5), p1, p1]
times = np.linspace(0, 1, num=NPTS)
curve = np.array([bezier(control_points, t) for t in times]).T
plt.plot(curve[0], curve[1])

bzPos = zip(*curve.tolist())



m = PyMouse()
for p in bzPos:
	print p
	m.move(p[0],p[1])
	sleep(2.0/NPTS)

