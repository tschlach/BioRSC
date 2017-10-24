"""
Author: Biohabitats Inc.
Updated: October 24, 2017

Asigns a suitability window to designer input points - outputs information about the associated attributes of the window

Dependencies:
	-Centerline and Window Classes
    -Rhino.Geometry as rg
    -rhinoscriptsyntax as rs

Tasks:
	-more robust reporting mechanism
	-need to clairify the role of 'input' vs. 'suitability' files
    -import window from suitability...
    -write window_from_points function

"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import suitability

user_points = #grasshopper component with several user defined points - could consider using rs.GetObeject??

curve = Centerline(crv)
curve.getParameters()

###Variables to display
windows = [] #a list of the window objects that will be output.
count = 0
text = []
tops = []

##This appends each of the window points to a large array - and draws the array. Doesn't actually give any control of the windows themselves
for i in user_points: ##'window start' will be an actual point - not an index...need to find a way to check for this...
    count += 1
    window = Window(curve.curve, i, curve.points, 30) ## 40 means 20 ft riffle test.
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
    #windows.append(window.window_pts)


def windows_from_points(points, riffle_span): #should we write out this function??

