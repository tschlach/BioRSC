import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 


V = rs.VectorCreate(A, B)
VUnit = rs.VectorUnitize(V)
length = rs.VectorLength(V)
print(length)

X = (A.X + B.X) / 2 - width * length * VUnit[1]
Y = (A.Y + B.Y) / 2 + width * length * VUnit[0]

pt = rs.coerce3dpoint((X, Y, A.Z))
C = rs.AddArc3Pt(A, B, pt)

