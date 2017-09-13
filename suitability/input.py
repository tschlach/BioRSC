"""
Assesses designer input points - draws potential riffles and outputs their 
"""
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

curve = Centerline(crv)

points = #user input points


for i in points:
	j = #get the actual closest point on the curve to the user input point - just in case there isn't snapping etc...
	window = Window(i, curve.curve, curve.points, window_width) #replace i with j if necessary...
	window.draw_riffle() ##this function needs to return the drawn riffle geometry...
	window.suitability() ##this will raise any red-flags on the suitability of drawing a riffle at that location