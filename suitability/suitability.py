"""
Author: Biohabitats Inc.
Updated: October 27, 2017

This script takes a centerline curve and returns the idealized riffle start locations, as determined by the 'suitability analysis'

Dependencies:
    -BioRSC Window and Curve class

Tasks:
    -testing windows of different length for suitability
    -returning riffle and pool suitability (currently only returns riffle tops)
"""

######
def create_window_dict(curve):
    windows = {}

    counts = ["%04d" % x for x in range(len(curve.points))] ##number of digits should reflect the number of segements/windows/assessment points on a line... 

    count = 0
    for i in curve.points:
        window = Window(curve.curve, i, curve.points, 40) ###would be nice to test this for different lengths...
        window.span_test()
        window.generate(window.span_test())
        window.getParameters()
        windows["Window" + counts[count]] = {
        "index": counts[count],
        "position_on_line": int(counts[count])/2,
        "slope": window.slope,
        "drop": window.drop,
        "p_ratio": window.p_ratio,
        "length": window.length,
        "start_height": window.start_height,
        "end_height": window.end_height
        }
        count += 1  

    return windows

#takes a list window dictionaries.
def suitability(windows):
    windows2 = []
    windows3 = []
    windows4 = []
    
    #p-ratio
    for key,value in windows.items():
        if value['p_ratio'] < 1:
            windows2.append(key)
    #drop
    for key, value in windows.items():
        if key in windows2:
            if value['drop'] < 0.25:
                windows3.append(int(value['index']))
    windows3.sort()
    
    #distance from other potential riffle starts
    for i in windows3:
        good_win = True
        for q in range (i - 50, i):
            if q in windows4:
                good_win = False
        if good_win:
            windows4.append(i)
    
    return windows4
