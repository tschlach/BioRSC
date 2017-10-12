"""
Author: Biohabitats Inc.
Updated: October 9, 2017

This script takes a centerline curve and returns the idealized riffle start locations, as determined by the 'suitability analysis'



Tasks:
    -the suitability file should take a centerline class and return idealized points for placing riffles (or points - or riffle/points)
    -weighting mechanism
    -testing windows of different length for suitability
    -create libraries from centerline and window -  def __init__():
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


#from window.py import window
#from centerline.py import centerline


######
##currently sudo code...
def suitability(centerline):
    attributes = {} ##attributes will be a dictionary with the structure {Window_ID : [attribute1, attribute2, attribute3]}
    for each point on the centerline:
        draw a window
        attributes['window_id'] = [window.attribute1, window.attribute2, window.attribute3]
    return riffle_starts
##
######


curve = Centerline(crv)
curve.getParameters()

a = suitability(curve) ##returns a set of points - the starts of riffle locations...