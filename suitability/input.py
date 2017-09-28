"""
Author: Biohabitats Inc.
Updated: September 28, 2017

Asigns designer input points

Dependencies:
	-window.py (need to import window.py eventually)

Tasks:

"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

curve = Centerline(crv)

user_points = #user input points

windows = [] #a list of the window objects that will be output.

##This just appends each of the window points to a large array - and draws the array. Doesn't actually give any control of the windows themselves
for i in user_points: ##'window start' will be an actual point - not an index...need to find a way to check for this...
    window = Window(curve.curve, i, curve.points, 40) ## 40 means 20 ft riffle test.
    window.generate()
    for i in window.window_pts:
        windows.append(rg.Point3d(i))