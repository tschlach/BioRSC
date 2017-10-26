"""
Author: Biohabitats Inc.
Updated: October 26, 2017

Asigns a suitability-assessment window to designer input points - outputs information about the associated attributes of the window

Dependencies:
	-Centerline and Window Classes
    -Rhino.Geometry as rg
    -rhinoscriptsyntax as rs

Tasks:
    -should be tied in with a iterative suitability analysis

"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import suitability

curve = Centerline(crv)
curve.getParameters()

##This appends each of the window points to a large array - and draws the array. Doesn't actually give any control of the windows themselves
##

def windows_from_points(curve, user_points, riffle_span):
    tops    = []
    text    = []
    count   = 0
    windows = []

    for i in user_points:
        count += 1
        window = Window(curve.curve, i, curve.points, riffle_span)
        window.generate()
        window.getParameters()
        tops.append(window.parameters[0])
        print('Window ' + str(count) + ' p-ratio: '+ str(window.p_ratio))
        print('Window ' + str(count) + ' drop: '+ str(window.drop))
        print('Window ' + str(count) + ' slope: '+ str(window.slope))
        print('\n')
        for i in window.window_pts:
            windows.append(rg.Point3d(i))
        text.append('window ' + str(count))

    return windows