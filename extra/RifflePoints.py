import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 
#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy

#x = Thalweg
#y = Division lengths for points along centerline
#z = Right Bank 
#u = Left Bank


class Centerline(object):
    def __init__(self, crvCenterline, crvBankRight, crvBankLeft, lenDivision):
        #****makes a list of each variable. In order, but not attributed to each point. 
        #****may want to pull everything under point info
        self.Thalweg = crvCenterline
        self.lenDivision = lenDivision
        self.BankRight = crvBankRight
        self.BankLeft = crvBankLeft
        self.length = rs.CurveLength(crvCenterline)             #Length
        self.start = rs.CurveStartPoint(crvCenterline)          #3D Start Point
        self.end = rs.CurveEndPoint(crvCenterline)              #3D End Point
        self.drop = self.start[2] - self.end[2]                 #Elevation Drop across length of curve
        self.points = rs.DivideCurveLength(crvCenterline, lenDivision, True, True) #Divide curve into lengths X (,X,,)
        self.riffles = []      

        #Set up Riffles
        self.createRiffles(lenDivision)
        
        #get existing conditions values
        #?????Should we do this after the getIdealRiffleDesign so that we can vary the window
        #?????based on the ideal riffle length? Answer: No. Ideal Riffle Design Requires Valley Slope.
        self.getSlopes(2,10)                #(,X) X is important and factors into variances alot. Need to not hard code in.
        self.getIdealRiffleDesign(.5, 10)
        self.getBendRatios(5)
        self.getBendRatios2(5)

        #calculate deisgn values
        
        
        #*****************************************
        #can now link this to the design iterator (justin) for riffle width and depth, using bank width as the riffle
        #width and plugging in a flowrate. 
        #*****************************************


     
        #Error handling/Print Values
        # for i in range(len(self.points)):
        #     print(self.riffles[i].station)
            # print(self.riffles[i].bend_ratio)
        #     print(self.riffles[i].slopeAtPoint)
        #     print(self.riffles[i].bank_width)
        #     print(self.riffles[i].pt)
        #     print(self.riffles[i].ptBankRight)
        #     print(self.riffles[i].ptBankLeft)
        #     print("----------")
        
    def getIdealRiffleDesign(self, riffle_drop_max, riffle_length_max): ##need an additional variable - that is able to be reset
        for i in self.riffles[0:160]:
            if i.valley_slope == 0: 
                pool_length = 10000
            else:  
                pool_length = abs((riffle_drop_max / i.valley_slope) - riffle_length_max)
            check = False
            count = 0
            riffle_drop_test = riffle_drop_max
            riffle_length_test = riffle_length_max
            while check == False and count < 35:
                print('STA=', i.station, '; Valley Slope=', i.valley_slope, '; PL=', pool_length, '; rLt=', riffle_length_test, '; rDt=', riffle_drop_test)
                if pool_length >= riffle_length_test:
                    i.riffle_length = riffle_length_test
                    i.riffle_drop = riffle_drop_test
                    i.riffle_slope = riffle_drop_test / riffle_length_test
                    i.geometry = "Riffle"
                    check = True
                else:
                    if riffle_length_test < 30:
                        riffle_length_test += 5
                        count +=1
                    elif riffle_drop_test < 2:
                        riffle_length_test = riffle_length_max
                        riffle_drop_test += 0.25
                        count +=1
                    else:
                        i.geometry = "Neither"
                        check = True
        return

    def createRiffles(self, lenDivision):
        for i in range(len(self.points)):
            station = i * lenDivision
            self.riffles.append(RifflePoint(self.points[i], self.Thalweg, self.BankRight, self.BankLeft, station))
        return
    

    def getBendRatios2(self, t):
        for i in range(len(self.riffles)-t):
            self.riffles[i].bend_ratio2 = rs.CurveCurvature(self.Thalweg, self.riffles[i].parameter)[3]
        return
        

    def getBendRatios(self, t):
        array_bend_ratio = []

        #get first list of bend_ratios
        for i in range(len(self.riffles)-t):
      
            p = horizontal_distance(self.riffles[i].ptBankLeft, self.riffles[i+t].ptBankLeft)
            l = abs(self.riffles[i].station - self.riffles[i+t].station)
            p_diff = abs(p - l)
            
            self.riffles[i].bend_ratio = p_diff
            array_bend_ratio.append(p_diff)

        #Normalize
        old_min = min(array_bend_ratio)
        old_range = max(array_bend_ratio) - old_min
        
        new_min = 0
        new_range = 1 - new_min

        for i in range(len(self.points)-t):
            n = self.riffles[i].bend_ratio
            new_bend_ratio = (n - old_min) / old_range * new_range + new_min
            self.riffles[i].bend_ratio = new_bend_ratio
        return


      
    #getSlopes defines the *discrete* slopes of the line, based on the straight distance between points on the line
    def getSlopes(self, winChannel, winValley):
        
        #Channel Slope
        for i in range(len(self.riffles) - winChannel):
            t1 = min([i, winChannel])
            t2 = min([len(self.riffles)-i, winChannel])
            sta1 = self.riffles[i - t1].station
            sta2 = self.riffles[i + t2].station
            pt1_z = self.riffles[i - t1].pt.Z
            pt2_z = self.riffles[i + t2].pt.Z
            self.riffles[i].channel_slope = (pt1_z - pt2_z)/(sta1 - sta2)

        #Valley Slope
        for i in range(len(self.riffles) - winValley):
            t1 = min([i, winValley])
            t2 = min([len(self.riffles)-i, winValley])
            sta1 = self.riffles[i - t1].station
            sta2 = self.riffles[i + t2].station
            pt1_z = self.riffles[i - t1].elevBankLow
            pt2_z = self.riffles[i + t2].elevBankLow
            self.riffles[i].valley_slope = (pt1_z - pt2_z)/(sta1 - sta2)          
        return


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

def horizontal_distance(pt1, pt2):
    distance = math.sqrt(math.pow(pt2.X - pt1.X, 2) + math.pow(pt2.Y - pt1.Y, 2)) 
    return distance

#x is set as curve in centerline class
crvRifflePoints = Centerline(crvThalweg, crvRightBank, crvLeftBank, interval)

    

attr = []
attr.append('pt.Z')
attr.append('parameter')
attr.append('tangent')
attr.append('slopeAtPoint')
attr.append('channel_slope')
attr.append('valley_slope')
attr.append('station')
attr.append('bend_ratio')
attr.append('ptBankRight')
attr.append('ptBankLeft')
attr.append('bank_width')
attr.append('BankRightIncision')
attr.append('BankLeftIncision')
attr.append('elevBankLow')
attr.append('valley_slope')
attr.append('riffle_length')
attr.append('riffle_slope')
attr.append('riffle_drop')
attr.append('riffle_width')
attr.append('geometry')

