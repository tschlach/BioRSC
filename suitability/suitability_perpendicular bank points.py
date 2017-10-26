Author: Biohabitats Inc.
Updated: October 26, 2017

#Produce points perpendicular to the vector of a point along the centerline.
#Output P - projected point information for both sides of alignment for comparison

import rhinoscriptsyntax as rs
import ghpythonlib.components as gc

P = []
#Input values
CL = rs.coercecurve(Crv)

smesh = rs.coercemesh(sitemesh)

#specimen perpendicular offset
frame = gc.XYPlane(0)
pt1 = gc.PointOriented(frame,0,x,0)
pt2 = gc.PointOriented(frame,0,-x,0)

#orienting specimen to every hframe instance
hframe = gc.HorizontalFrame(CL, t)
opt1 = gc.Orient(pt1, frame, hframe).geometry
opt2 = gc.Orient(pt2, frame, hframe).geometry

#projecting offset point to site mesh
neg20 = gc.Negative(20)
zdir20 = gc.UnitZ(neg20)
move1 = gc.Move(opt1, zdir20).geometry
move2 = gc.Move(opt2, zdir20).geometry

zdir = gc.UnitZ(1)
projpt1 = gc.ProjectPoint(move1, zdir, smesh).point
projpt2 = gc.ProjectPoint(move2, zdir, smesh).point

P.append(projpt1)
P.append(projpt2)