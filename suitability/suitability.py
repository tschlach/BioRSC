"""
Author: Biohabitats Inc.
Updated: October 9, 2017

This script takes a centerline curve and returns the idealized riffle start locations, as determined by the 'suitability analysis'

Dependencies:
    -rhinoscriptsyntax as rs
    -BioRSC Window Class
    -BioRSC Centerline Class

Tasks:
    -the suitability file should take a centerline class and return idealized points for placing riffles (or points - or riffle/points)
    -weighting mechanism
    -testing windows of different length for suitability
    -create libraries from centerline and window -  def __init__():
    -read and recreate suitability_oct7.py
"""

######
##currently sudo code
def suitability(windows):
    attributes = {} ##attributes will be a dictionary with the structure {Window_ID : [attribute1, attribute2, attribute3]}
    for each point on the centerline:
        draw a window
        attributes['window_id'] = [window.attribute1, window.attribute2, window.attribute3]
    return riffle_starts
##
######

####
########
######## This is the current code that will output the window attributes for a curve
######## The output is a dictionary
######## The output is then put into... the suitability script and 
########
####
curve = Centerline(crv)
curve.getParameters()
curve.getSlopes()

windows = {}

count = 0
for i in curve.points:
    window = Window(curve.curve, i, curve.points, 40)
    window.span_test()
    window.generate(window.span_test())
    window.getParameters()
    count += 1
    windows['Window' + str(window.start_index)] = [window.start_index, window.length, window.slope, window.drop, window.p_ratio]

print(windows)