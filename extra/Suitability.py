import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 

#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy


TierR1 = []
TierR2 = []
TierR3 = []
TierP1 = []
TierNull = []

def get_VariableArray(centerline):

    w, h = 14, len(centerline.riffles)
    arrVariables = [[None] * w for i in range(h)]
    
    c = 0
    # print(arrVariables)
 
    for i in centerline.riffles:     #i = RifflePoint Class feature

        arrVariables[c][0] = c
        arrVariables[c][1] = i.station 
        arrVariables[c][2] = i.bend_ratio2  #i.bend_ratio
        arrVariables[c][3] = i.bank_width
        arrVariables[c][4] = i.BankRightIncision
        arrVariables[c][5] = i.BankLeftIncision
        arrVariables[c][6] = i.elevBankLow
        arrVariables[c][7] = i.valley_slope
        arrVariables[c][8] = i.riffle_length
        arrVariables[c][9] = i.riffle_slope
        arrVariables[c][10] = i.riffle_drop
        arrVariables[c][11] = i.riffle_width
        arrVariables[c][12] = i.geometry
        arrVariables[c][13] = i.pt.Z 
        # arrVariables[c][x] = 
        # arrVariables[c][x] = i.parameter
        # arrVariables[c][x] = i.tangent
        # arrVariables[c][x] = i.slopeAtPoint
        # arrVariables[c][x] = i.channel_slope
        # arrVariables[c][x] = i.valley_slope
        # arrVariables[c][x] = i.pt
        # arrVariables[c][x] = i.ptBankRight
        # arrVariables[c][x] = i.ptBankLeft 

        c = c + 1
   
    return  arrVariables

def maxList(l, v):
    #l = 2D list of variables
    #v = variable looking for 
    max_val = None
    num = None

    for i in range(len(l)):
        if l[i][v] > max_val:
            max_val = l[i][v]
            max_idx = l[i][0]
            num = i
            print(max_val)
    return max_idx, max_val, num

def minList(l, v):
    #l = 2D list of variables
    #v = variable looking for 
    min_val = None
    num = None

    for i in range(len(l)):
        if l[i][v] < min_val:
            min_val = l[i][v]
            min_idx = l[i][0]
            num = i
    return min_idx, min_val, num

def nearestList(l, v, value):
    #l = 2D list of variables
    #v = variable looking for
    #value = value looking for nearest to 
    min_d = 100000000000
    near_val = None
    num = None

    for i in range(len(l)):
        d = abs(l[i][v]-value)
        if d < min_d:
            near_val = l[i][v]
            near_idx = l[i][0]
            min_d = d
            num = i

    return near_idx, near_val, num

def get_RiffleTiers(list2D):

    #Filter 1
    for i in range(len(list2D)):
        if list2D[i][12] == "Riffle":                   #Geometry Check
            if list2D[i][2] > 10:                       #Bend_ratio Check (value random, need to select)
                TierR1.append(list2D[i])
            elif list2D[i][2] > 5:
                TierR2.append(list2D[i])
            else:
                TierR3.append(list2D[i])
        elif list2D[i][12] == "Pool":                   #Geometry Check
            TierP1.append(list2D[i])
        else:
            TierNull.append(list2D[i])
    return

def place_Riffles(centerline):
    
    print("----------")
    print("TierR1, length=", len(TierR1))
    #print(TierR1)
    print("----------")

    listFinal = []
    listFinal.append(centerline.riffles[0])
    removeLowerLimit = None
    removeUpperLimit = None
    #deleteRange = range()

    #+++++++++++
    #search 1
    #+++++++++++
    #Loop Through values (while?)
    #Get Max Value (just bend for now, later to be a weighted value)
    index1, value, i = maxList(TierR1, 2)
        #index1 = index in Riffles
        #i = index in TierR1

    #Append to final List
    listFinal.append(centerline.riffles[index1])

    #get riffle/pool length
    rCurrent = centerline.riffles[index1]
    rSTA = rCurrent.station
    print_RiffleInfo(rCurrent, index1)

    #delete from Tier
    TierR1.remove(TierR1[i])

    #++++++++++++++++++++++++++++++++++++++++++++++
    #Search 2
    #++++++++++++++++++++++++++++++++++++++++++++++
    #assume pool length = riffle length
    #this will need to be adjusted later more intelligently

    #Loop Through
    #Look downstream at next value distance down of riffle and pool length from last
    #find station nearest to end of US riffle
    print("Looking Downstream")

    targetSTA = rCurrent.station + rCurrent.riffle_length + rCurrent.riffle_length
    targetElev = rCurrent.pt.Z - rCurrent.riffle_drop
    t = i
    
    removeLowerLimit = rSTA
    removeUpperLimit = targetSTA

    while t < len(TierR1):
        print(t)
        index2, t = find_NextDSRiffle(TierR1, t, targetSTA, targetElev)
        print(t)
        
        if index2 != None:
            listFinal.append(centerline.riffles[index2])
            rCurrent = centerline.riffles[index2]
            targetSTA = rCurrent.station + rCurrent.riffle_length + rCurrent.riffle_length
            targetElev = rCurrent.pt.Z - rCurrent.riffle_drop
            removeUpperLimit = targetSTA
            print_RiffleInfo(rCurrent, index2)
        else:
            t = len(TierR1)

    print("Lower Limit=", removeLowerLimit, '; Upper Limit=', removeUpperLimit)
    
    delete_Riffles(removeLowerLimit, removeUpperLimit)

    #Loop Through
    '''
    Look upstream at next value distance down of riffle and pool length from last
    If yes
        #add to final list
        #delete from tier
    if no, set up loop to look in either direction by a specific amount
    '''

    #Reset i to original value from first Riffle
    #get riffle/pool length of first riffle
    rCurrent = centerline.riffles[index1]
    targetSTA = rCurrent.station 
    targetElev = rCurrent.pt.Z 
    print("Looking Upstream")
    t = i

    while t > 0:
        print(t)
        index2, t = find_NextUSRiffle(TierR1, t, targetSTA, targetElev)
        print(t)
        
        if index2 != None:
            listFinal.append(centerline.riffles[index2])
            rCurrent = centerline.riffles[index2]
            targetSTA = rCurrent.station 
            targetElev = rCurrent.pt.Z 
            print_RiffleInfo(rCurrent, index2)
        else:
            t = 0    
    # print(listFinal)

        

    print("----------")
    print("TierR1, length=", len(TierR1))
    #print(TierR1)
    print("----------")

    return listFinal


def print_RiffleInfo(l, i):
    print("----------")
    print("index = ", i)
    print("Station = ", l.station)
    print("Invert Elev = ", l.pt.Z)
    print("Riffle Drop = ", l.riffle_drop)
    print("Riffle Length = ", l.riffle_length)
    print("Radius of Curvature = ", l.bend_ratio2)
    return

def delete_Riffles(iLower, iUpper):
    #iLower, iUpper are Stations within Tier classes

    print("----------")
    print("Delete Riffles")
    print("Total Count=", len(listVariables), 'Final Station=', listVariables[-1][1])
    print('R1 Count=', len(TierR1))

    #Tried to make a separate function but it didn't work. Should come back to it.
    i=0
    while i < len(TierR1):
        print("----------")
        print(len(TierR1))
        print('i=', i)
        print(TierR1[i][1])
        if iLower <= TierR1[i][1] < iUpper:
            print('Delete:',TierR1[i][1], TierR1[i][0], TierR1[i])
            TierR1.remove(TierR1[i])                #
            print(len(TierR1))
            print('i=', i)
        else:
            i += 1

    i = 0
    while i < len(TierR2):
        print("----------")
        print(len(TierR2))
        print('i=', i)
        print(TierR2[i][1])
        if iLower <= TierR2[i][1] < iUpper:
            print('Delete:',TierR2[i][1], TierR2[i][0], TierR2[i])
            TierR2.remove(TierR2[i])                
            print(len(TierR2))
            print('i=', i)
        else:
            i += 1
    i = 0
    while i < len(TierR3):
        print("----------")
        print(len(TierR3))
        print('i=', i)
        print(TierR3[i][1])
        if iLower <= TierR3[i][1] < iUpper:
            print('Delete:',TierR3[i][1], TierR3[i][0], TierR3[i])
            TierR3.remove(TierR3[i])                
            print(len(TierR3))
            print('i=', i)
        else:
            i += 1

    print('R1 Count=', len(TierR1))
    print("End Delete Riffles")
    print("----------")
    return

def find_NextDSRiffle(l, t, targetSTA, targetElev):
    #targetSTA = station of end of pool based on station of current riffle, length
    #            of riffle, and length of pool
    #targetElev = Elevation of current riffle - drop of current riffle

    print('target:', targetSTA, targetElev)
    for i in range(t, len(l)):
        rNext = l[i]

        print(rNext[1], rNext[13])

        #Check length from previous
        if rNext[1] >= targetSTA: 
            #Check that invert is within 0.1ft of target invert
            if abs(rNext[13]-targetElev) < 0.1:
                index = rNext[0]
                return index, i
    return None, i

def find_NextUSRiffle(l, t, targetSTA, targetElev):
    #targetSTA = Station of current Riffle
    #targetElev = Elevation of current riffle

    print('t = ', t)
    print('target:', targetSTA, targetElev)
    #print("i = ", i)
    #Loop Through upstream Riffles
    for i in range(t-1, 0, -1):       #could try reversed(range()), may be faster
        #gets next US Riffle
        rNext = l[i]

        #Consider just making this a variable of the riffle (targetSTA)
        #rNext_EndStation = rSTA + rL + pL
        rNext_EndStation = rNext[1] + rNext[8] + rNext[8] 
        
        #rNext_EndElev = Elevation - Drop
        rNext_EndElev = rNext[13] - rNext[10]

        print(rNext[1], rNext[13], rNext[10], rNext_EndStation, rNext_EndElev)

        #End of Pool for US Riffle needs to be before targetSTA
        if rNext_EndStation <= targetSTA: 
            #Check that invert is within 0.1ft of target invert
            if abs(rNext_EndElev-targetElev) <= 0.1:
                index = rNext[0]
                return index, i
    return None, i

def suitability(centerline):
    
    Tier1 = []
    Tier2 = []
    Tier3 = []
    
    for i in range(len(centerline.riffles)):
        if centerline.riffles[i].geometry == "Riffle":
            if centerline.riffles[i].bend_ratio2 >200:
                Tier1.append(centerline.riffles[i])

    sortArray = []
        
    for i in Tier1:
        sortArray.append(int(i.station))
        good_win = True
        for q in range(int(i.station - 25), int(i.station)):
            if q in sortArray:
                good_win = False
        if good_win == True:
            Tier2.append(i)

    return Tier2


    #Filter1
    #add RifflePoint features to Tier1 Array
    #for i in range(len(centerline.riffles)):
    #    if centerline.riffles[i].geometry == "Riffle":
    #        if centerline.riffles[i].bend_ratio < .18:       #to be replaced with Tyler's update
    #            Tier1.append(centerline.riffles[i])

    #Tier1
    #riffles.geometry - Check riffle Geometry has as a Riffle
    #riffles.bend_ratio - Check that it is straight enough for Riffle
    #Based on: riffles.geometry, riffles.bend_ratio


    #Tier2
    #riffles.riffleWidth - prefer to use least rock, so prioritize narrower riffles 
        #(note: riffle width should be calculated so that appropriate width/depth
        # is calculated in first place)
    #Riffles.BankRightIncision - smaller depths better for placement for less stone?
    #Riffles.BankLeftIncision - smaller depths better for placement for less stone?


    #Where to place these in Suitability???
        #riffles.slope 
        #riffles.station
        #riffles.riffle_length 
        #riffles.RiffleSlope
        #riffles.RiffleDrop 

    #Suitability steps:
    #Step 1: Check 

    #Tier1
#    for i in Tier1:
#        print(i.station)
#        print(i)

    #sortArray = []
    #print(Tier1)
    #Tier_new = sorted(Tier1, Tier1.riffles.bend_ratio)
    
#    for i in Tier1:
        
        # good_win = True
        # for q in range (i - 50, i):
        #     if q in windows4:
        #         good_win = False
        # if good_win == True:
        #     windows4.append(i)
    #arrSort = [,,]    #[i, station, bend_ratio]
        
    #for i in Tier1:





    #    print(i.station)
    #    print(i.bend_ratio)

    #return Tier1

listVariables = get_VariableArray(crvRifflePoints)

get_RiffleTiers(listVariables)
Riffles = place_Riffles(crvRifflePoints)


# print("TierR1")
# print(TierR1)
# print("TierR2")
# print(TierR2)
# print("TierR3")
# print(TierR3)
# print("TierP1")
# print(TierP1)
# print("TierNull")
# print(TierNull)  

#Riffles = suitability(crvRifflePoints)
# print(Riffles)