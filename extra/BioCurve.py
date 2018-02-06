import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 




if width == None:		
	width = 0
if depth == None:		
	depth = 0
if offset == None:		
	offset = 0
if drop ==None:
	drop = 0

P_R = rs.coerce3dpoint((pt.X - 0.5 * width * T[1] + offset * T[0], pt.Y + 0.5 * width * T[0] + offset * T[1], pt.Z - drop))
P_L = rs.coerce3dpoint((pt.X + 0.5 * width * T[1] + offset * T[0], pt.Y - 0.5 * width * T[0] + offset * T[1], pt.Z - drop))
P_C = rs.coerce3dpoint((pt.X + offset * T[0], pt.Y + offset * T[1], pt.Z - depth - drop))
C = rs.AddArc3Pt(P_R, P_L, P_C)
line = rs.AddLine(P_R, P_L)


