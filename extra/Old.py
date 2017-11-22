Old

def get_RiffleTiers(list_values):

    #Filter 1
    for i in range(len(list_values)):
        if list_values[i][12] == "Riffle":                   #Geometry Check
            if list_values[i][2] > 10:                       #Bend_ratio Check (value random, need to select)
                TierR1.append(list_values[i])
            elif list_values[i][2] > 5:
                TierR2.append(list_values[i])
            else:
                TierR3.append(list_values[i])
        elif list_values[i][12] == "Pool":                   #Geometry Check
            TierP1.append(list_values[i])
        else:
            TierNull.append(list_values[i])
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
    retur

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
    return None, Non

def get_VariableArray(centerline):

    w, h = 14, len(centerline.riffles)
    list_values = [[None] * w for i in range(h)]
        
    c = 0
    # print(list_values)
 
    for i in centerline.riffles:     #i = RifflePoint Class feature

        list_values[c][0] = i.index
        list_values[c][1] = i.station 
        list_values[c][2] = i.bend_ratio2  #i.bend_ratio
        list_values[c][3] = i.bank_width
        list_values[c][4] = i.BankRightIncision
        list_values[c][5] = i.BankLeftIncision
        list_values[c][6] = i.elevBankLow
        list_values[c][7] = i.valley_slope
        list_values[c][8] = i.riffle.length
        list_values[c][9] = i.riffle.slope
        list_values[c][10] = i.riffle.drop
        list_values[c][11] = i.riffle.width
        list_values[c][12] = i.geometry
        list_values[c][13] = i.pt.Z 
        # list_values[c][x] = 
        # list_values[c][x] = i.parameter
        # list_values[c][x] = i.tangent
        # list_values[c][x] = i.slopeAtPoint
        # list_values[c][x] = i.channel_slope
        # list_values[c][x] = i.valley_slope
        # list_values[c][x] = i.pt
        # list_values[c][x] = i.ptBankRight
        # list_values[c][x] = i.ptBankLeft 

        c += 1
   
    return  list_value