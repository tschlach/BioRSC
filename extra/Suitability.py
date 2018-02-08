import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import math 
from operator import itemgetter

#import numpy as np     #Doesnt' work for IronPython. Need to download stuff... Look at this link: 
        #https://stevebaer.wordpress.com/2011/06/27/numpy-and-scipy-in-rhinopython/
        #http://www.grasshopper3d.com/forum/topics/scipy-and-numpy


def calculate_Suitability(centerline):

    #Filter 1
    for i in centerline.riffles:
        if i.geometry == "Riffle":                   #Geometry Check
            i.suitability = i.curvature

        elif i.geometry == "Pool":                   #Geometry Check
            i.suitability = -i.curvature

        else:
            i.suitability = 0

    return 


#___________________________________________________________________________
#STEP 0: RESET Suitability
#___________________________________________________________________________
print('STEP 0---------------')
for i in crvRifflePoints.riffles:
   i.suitability = None

# print('# of Stream Points =', len(crvRifflePoints.riffles))

for i in crvRifflePoints.riffles:
    print(i.geometry, i.suitability)


    
#___________________________________________________________________________
#STEP 1: GET WEIGHTING
#___________________________________________________________________________
# print(Weights)




#___________________________________________________________________________
#STEP 1: CALCULATE STREAM POINT SUITABILITIES
#Adjust the riffles.suitability values for each stream points
#___________________________________________________________________________
print('STEP 1---------------')
calculate_Suitability(crvRifflePoints)
#Print Suitability Here*********************************

for i in crvRifflePoints.riffles:
    print(i.geometry, i.suitability)


