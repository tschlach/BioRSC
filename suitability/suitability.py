"""
Author: Biohabitats Inc.
Updated: November 16, 2017

A series of functions that outputs ideal riffle start locations - based on their overall suitability...

Dependencies: rhinoscriptsyntax as rs, Rhino.Geometry as rg, math

Tasks:
    -Calculating basic statistics on our variable array?
    -appending to and writing a log - vs. printing throughout the script
    -combine similar functions - minList/maxList/nearestList - findUpstream/findDownstream
    -
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 

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
            if list2D[i][2] > 10:                       #Bend_ratio Check (value random, need to select - top 10%)
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
    #Loop Through values
    #Get Max Value (just bend for now, later to be a weighted value)
    while len(TierR1) != 0:
        index1, value, i = maxList(TierR1, 2)
            #index1 = index in Riffles ###??? - TS.
            #i = index in TierR1

        #Append to the final list the riffle point in Tier1 that has the maximum bend ratio value (ie. is 'straightest')
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

        targetSTA = rCurrent.station + rCurrent.riffle_length + rCurrent.riffle_length ##does this need to be riffle_length * 2 - asking the question 
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
        
        removeUpperLimit = targetSTA 

        while t > 0:
            print(t)
            index2, t = find_NextUSRiffle(TierR1, t, targetSTA, targetElev)
            print(t)
            
            if index2 != None:
                listFinal.append(centerline.riffles[index2])
                rCurrent = centerline.riffles[index2]
                targetSTA = rCurrent.station 
                targetElev = rCurrent.pt.Z
                removeLowerLimit = targetSTA 
                print_RiffleInfo(rCurrent, index2)
            else:
                t = 0          


        print("Lower Limit=", removeLowerLimit, '; Upper Limit=', removeUpperLimit)
        
        delete_Riffles(removeLowerLimit, removeUpperLimit)


        print("----------")
        print("TierR1, length=", len(TierR1))
        #print(TierR1)
        print("----------")

    print(TierR1)

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
    return None, None



listVariables = get_VariableArray(crvRifflePoints)

get_RiffleTiers(listVariables)

print(TierR1)

print("TierNull:", TierNull)

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