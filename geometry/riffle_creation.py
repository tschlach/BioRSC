#Title: riffle_creation.py
#Author: Biohabitats Inc.
#Updated: October 26, 2017

#Dependencies:
import rhinoscriptsyntax as rs
import ghpythonlib.components as gc

#Creation of arc's based on defined points and develop a surface between them.

Loft = []
def Riffle_Creation(f_tor, f_bor, thals, Rw, Rd):
    #f_tor - hframe top of riffle, f_bor - hframe bottom of riffle, thals - thalweg start, Rw - riffle width, Rd - riffle depth
    Rwpos = (float(Rw) * .5)
    Rwneg = gc.Negative(Rwpos)
    thals = rs.coerce3dpoint(thals)
    #top arc creation
    pt_top1 = gc.PointOriented(f_tor, u, Rwpos, Rd)
    pt_top2 = gc.PointOriented(f_tor, u, Rwneg, Rd)
    arc_top = gc.Arc3Pt(pt_top1, thals, pt_top2).arc
    #bottom arc creation
    pt_bot1 = gc.PointOriented(f_bor, u, Rwpos, Rd)
    pt_bot2 = gc.PointOriented(f_bor, u, Rwneg, Rd)
    pt_bot3 = gc.PointOriented(f_bor, u, v)
    arc_bot = gc.Arc3Pt(pt_bot1, pt_bot3, pt_bot2).arc
    #loft riffle creation
    rif_loft = gc.Loft([arc_top, arc_bot])
    Loft.append(rif_loft)
    return

Riffle_Creation(f_tor, f_bor, thals, Rw, Rd)