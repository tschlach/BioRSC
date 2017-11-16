"""
Author: Biohabitats Inc.
Updated: November 16, 2017

Defines the centerline class, the attributes of which can be used to inform the window class when making a suitability assessment

Dependencies: rhinoscriptsyntax as rs, Rhino.Geometry as rg, math

Inputs
    curve: a single Rhino curve

Tasks:
    -should the window class inherent Centerline attributes?
"""
class Centerline(object):
    def __init__(self, crvCenterline, crvBankRight, crvBankLeft, lenDivision):
        self.Thalweg = crvCenterline
        self.lenDivision = lenDivision
        self.BankRight = crvBankRight                           ##may be able to set these as offsets of the centerline to decrease the inputs to the python component...
        self.BankLeft = crvBankLeft
        self.length = rs.CurveLength(crvCenterline)             #Length
        self.start = rs.CurveStartPoint(crvCenterline)          #3D Start Point
        self.end = rs.CurveEndPoint(crvCenterline)              #3D End Point
        self.drop = self.start[2] - self.end[2]                 #Elevation Drop across length of curve
        self.points = rs.DivideCurveLength(crvCenterline, lenDivision, True, True) #Divide curve into lengths X (,X,,)
        self.riffles = []      

        #Set up Riffles
        self.createRiffles(lenDivision)
        
        self.getSlopes(2,5)
        self.getIdealRiffleDesign(.5, 10)
        self.getBendRatios(5)
        self.getBendRatios2(5)
    
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

###
###Idea riffle design function sets the geometry attribute of each riffle point - by checking whether a proposed riffle location will 
###
    def getIdealRiffleDesign(self, riffle_drop_min, riffle_length_min):
        for i in self.riffles[0:len(self.riffles) - riffle_length_min]:
            
            check = False
            count = 0
            riffle_drop_test = riffle_drop_min
            riffle_length_test = riffle_length_min
            
            #Count is an iterator that keeps the while loop from running infinitely
            while check == False and count < len(self.riffles) - riffle_length_min:
                if i.valley_slope == 0: 
                    pool_length = 10000
                else:  
                    pool_length = abs((riffle_drop_test / i.valley_slope) - riffle_length_test)
                #print('STA=', i.station, '; Valley Slope=', i.valley_slope, '; PL=', pool_length, '; rLt=', riffle_length_test, '; rDt=', riffle_drop_test)
                if pool_length >= riffle_length_test:
                    i.riffle_length = riffle_length_test
                    i.riffle_drop = riffle_drop_test
                    i.riffle_slope = riffle_drop_test / riffle_length_test
                    i.geometry = "Riffle"
                    check = True
                else:
                    if riffle_length_test < 30: ##may want to have this length as an arg input for the function
                        riffle_length_test += 5 ##adds five feet - but may be able to set this as difference in station distance
                        count +=1
                    elif riffle_drop_test < 2:
                        riffle_length_test = riffle_length_min
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