"""
Author: Biohabitats Inc.
Updated: October 12, 2017

D50 functions - used for determining stone sizing 

Inputs:

Tasks:

"""
# D50 is the stone size for 50% passing
import math
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


# Constant/Starting values
g = 32.2   # ft/s
DensityWater = 62.5
counter1 = 0
counter2 = 0
Result1 = False
Result2 = False
S = Slope_Riffle

# Initial guesses for iterations
D50 = 3
d_flow = .1

# WaterSurface Slope Calculation
CLcurve = rs.coercecurve(Centerline)
ptStart = rs.CurveStartPoint(CLcurve)
ptEnd = rs.CurveEndPoint (CLcurve)
CrvLength = rs.CurveLength(CLcurve)

SlopeWS = abs((ptStart[2] - ptEnd[2]) / CrvLength)

# Iteration Step 1
while Result1 == False:
    Result2 = False
    counter2 = 0
    
    while Result2 == False:
        W = Wchannel / (-d_channel / d_flow) ** 0.5
        Wp = W + (8 * d_flow ** 2 / (3 * W))
        A = 2 / 3 * d_flow * W
        Rh = A / Wp
        n = (d_flow ** (1 / 6)) / ((21.6 * math.log10(d_flow * 12 / D50)) + 14)
        V = (1.486 / n) * Rh ** (2 / 3) * S ** 0.5
        Qchannel = V * A
        
        # Calc variables for d_critical
        cr_d = d_flow * 1.2    # 1.2 = factor of safety
        cr_W = Wchannel / (-d_channel / cr_d) ** 0.5
        cr_Wp = cr_W + (8 * cr_d ** 2 / (3 * cr_W))
        cr_A = 2 / 3 * cr_d * cr_W
        cr_Rh = cr_A / cr_Wp
        cr_n = (cr_d ** (1 / 6)) / ((21.6 * math.log10(cr_d * 12 / D50)) + 14)
        cr_V = (1.486 / cr_n) * cr_Rh ** (2 / 3) * S ** 0.5
        cr_Fr = cr_V / math.sqrt(g * cr_d)    # not actual critical depth, but finding froude number at a flow depth 1.2*dflow
        
        if cr_Fr < 1.0:
            cr_C = 1.20 # Subcritical           
        else:
            cr_C = 0.86 # Supercritical
        
        # Calculate Maximum Velocity for Stone Size D50
        Vmax = cr_C * (2 * g * ((DensityStone - DensityWater) / DensityWater)) ** 0.5 * (D50 / 12) ** 0.5
        
        # Check that Qchannel is greater than Qdesign
        if Qchannel > Qdesign:
          Result2 = True
          Answer = "Counter2 = " + str(counter2) + "; " + str(V)
        else:
          Result2 = False
          d_flow += 0.01
          counter2 += 1
        
        if counter2 == 1000:
          Answer = "Calculations did not converge; Counter2=" + str(counter2)
          Result2 = True
        
    # Check that V is less than Vmax
    if V < Vmax:
        Result1 = True
        Answer += "Counter1=" + str(counter1)
    else:
        Result1 = False
        d_flow = 0.1
        D50 += 1
        
    counter1 += 1
    if counter1 == 50:
        Answer += "Calculations did not converge; Counter1=" + str(counter1) + "; V=" + str(V)
        Result1 = True

Area = A
Wtop = W
Qcheck = Qchannel