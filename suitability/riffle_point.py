"""
Author: Biohabitats Inc.
Updated: November 16, 2017

Dependencies: rhinoscriptsyntax as rs, Rhino.Geometry as rg, math

Inputs

Tasks:
    -need to add an 'index' attribute of the RifflePoint object - to identify it's poisition along the line... this comes up frequently in operations w/in the suitability.py file
"""

class RifflePoint(object):
    """docstring for ClassName"""
    #Notes to think about:
    # -Does difference in left/right bank elevation matter in design?

    def __init__(self, point, crvCenterline, crvBankRight, crvBankLeft, station):
        #Define Initial Values
        self.pt = point
        self.parameter = rs.CurveClosestPoint(crvCenterline, point)     #Parameter (t) for point on centerline
        self.tangent = rs.CurveTangent(crvCenterline, self.parameter)
        self.slopeAtPoint = self.tangent[2]
        self.channel_slope = None
        self.valley_slope = None
        self.station = station
        self.bend_ratio = None
        self.bend_ratio2 = None

        #Bank Information
        self.ptBankRight = rs.EvaluateCurve(crvBankRight, rs.CurveClosestPoint(crvBankRight, self.pt))
        self.ptBankLeft = rs.EvaluateCurve(crvBankLeft, rs.CurveClosestPoint(crvBankLeft, self.pt))
        self.bank_width = horizontal_distance(self.ptBankRight, self.ptBankLeft)
        self.BankRightIncision = self.ptBankRight.Z - self.pt.Z 
        self.BankLeftIncision = self.ptBankLeft.Z - self.pt.Z 
        self.elevBankLow = min(self.ptBankLeft.Z, self.ptBankRight.Z)
        self.valley_slope = None

        #Proposed Riffle Design Information
        self.riffle_length = None
        self.riffle_slope = None
        self.riffle_drop = None
        self.riffle_width = None     #Calc based on Bank Width
        self.geometry = None

               
        #project Thalweg to Horizontal Plane
        crvCenterlineHoriz = crvCenterline
        rs.ScaleObject(crvCenterlineHoriz, (0,0,0), (1,1,0))
        self.parameterHorizontal = rs.CurveClosestPoint(crvCenterlineHoriz, point)