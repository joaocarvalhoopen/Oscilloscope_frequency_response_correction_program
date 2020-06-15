# Name: Extract_attenuation_values_from_scope_FFT_image.py
# Description: This program was made to get all the data points of the graph with
#              the most possible accurate values from the following frequency
#              response antenation measurement PNG graph image.
#              The output of this program will be a file containing
#              table of points, with Frequency vs Attenuation in dBV and volt
#              scale factor.
#              This program was made specifically for the FFT output of
#              the Siglent SDS2000X plus series but can be adapted for a 
#              different scope image that has similar characteristics.   
#              You can add as many zones as you need, to segment the graph
#              search area by parameterizing the program config variables.
#
# IMPORTANTE: This input image was used because I needed a very accurate measurement
#             of the scopes frequency response, with a good RF signal generator.
#             At the time this was the best / more accurate graph I could find
#             to extract data points. 
#             The scope was a Siglent SDS2354X-Plus Full range 570 MHz -3 dB. 
#
#
# EEVBlog project thread:
#  https://www.eevblog.com/forum/testgear/oscilloscope-frequency-response-correction-program/
#
# GitHub project page:
#  https://github.com/joaocarvalhoopen?tab=repositories
#
#
# Input image: "SDS2354Xplus 2GSa 8bit 1GHz.png"
# Source of image: The post on EEVBlog Forum from the member Performa01 on
#                  the topic "Siglent SDS2000X Plus", inside the area
#                  "Test Equipment"  . 
#  https://www.eevblog.com/forum/testgear/siglent-sds2000x-plus-coming/msg2787168/#msg2787168
#
# Program author: João Nuno Carvalho
# Date:           2020.06.14
# License:        MIT Open Source License
#
# Note 1: In the graph image ploted line, there are points in the vertical
#         axes with more then one connected pixel. In this case the pixel
#         position that will be used is the vertical average of the connected
#         pixels.
#
# Note 2: With Paint.net I obtained the following info from the PNG graph image.
#        -Image resolution (length_x X length_y): 1024x600
#        -Color of trace in HEX: B014E8
#        -Color of left graph position left measuring markers in HEX: B014E8    
#
#        -First graph position 0dbV ref position (freq a little over 0Hz,
#        0Hz is at pos x:19): x:34 y:116    
#        -Last signal attenuation position in graph image: x:825 y:530
#        -Upper limit signal position: y:110
# 
#        -Search zones so it doesn't interfere with vertical (left) markings
#        of dbV width the same color code.
#              Search Zone A:
#                          -upper left corner: x:34 y:110
#                          -down right corner: x:82 y:157
#   
#              Search Zone B:
#                          -upper left corner: x:83  y:110
#                          -down right corner: x:873 y:530
#   
# Note 3: Attenuation grid image Y position values for -dBV scale:
#         pos y:104 value: -12 dbV  (greater then upper signal line plot bound)
#         pos y:164 value: -14 dbV
#         pos y:224 value: -16 dbV
#         pos y:285 value: -18 dbV
#         pos y:345 value: -20 dbV
#         pos y:406 value: -22 dbV
#         pos y:465 value: -24 dbV
#         pos y:525 value: -26 dbV  
#         pos y:??? value:  ??      (there is one more that must be calculated,
#                                    because it's lower then a -2 dBV step,
#                                    lower then -26 dBV)
#
#
# Note 4:  Frequency grid image X position values for MHz scale:
#         pos x:18  value:    0 MHz
#         pos x:104 value:  100 MHz
#         pos x:190 value:  200 MHz
#         pos x:275 value:  300 MHz
#         pos x:360 value:  400 MHz
#         pos x:445 value:  500 MHz
#         pos x:531 value:  600 MHz
#         pos x:616 value:  700 MHz
#         pos x:701 value:  800 MHz
#         pos x:787 value:  900 MHz
#         pos x:872 value: 1000 MHz
# 
# 


from PIL import Image
import math
import numpy as np
import csv

################
# Configurations
################

fileImgIn  = "SDS2354Xplus_2GSa_8bit_1GHz.png"

# Flags that control the drawing of the markings.
flag_mark_4_corners_graph_limits  = False  # True   False
flag_plot_extracted_signal_points = True   # True   False
flag_mark_left_grid_Y_points      = True   # True   False
flag_mark_bottom_grid_X_points    = True   # True   False

# The hex byte for each R, G, B component of the attenuation graph line color.
signalColorR = 0xB0
signalColorG = 0x14
signalColorB = 0xE8

# The hex byte for each R, G, B component of the color point extracted over
# the graph line.
outputSignalMarkerColorR = 0xFF
outputSignalMarkerColorG = 0xFF
outputSignalMarkerColorB = 0xFF

# The hex byte for each R, G, B component of the color of points of the extended
# first points of the graph line. This points are extended with the 0 dBV reference
# value, like points to the right, the flattest region in the signal graph line.
outputSignalMarkerInitialExtensionColorR = 0xFF
outputSignalMarkerInitialExtensionColorG = 0x00
outputSignalMarkerInitialExtensionColorB = 0x00

# The hex byte for each R, G, B component of the grid Y color point.
outputGrid_Y_MarkerColorR = 0x00
outputGrid_Y_MarkerColorG = 0xFF
outputGrid_Y_MarkerColorB = 0x00

# The hex byte for each R, G, B component of the grid X color point.
outputGrid_X_MarkerColorR = 0x00
outputGrid_X_MarkerColorG = 0xFF
outputGrid_X_MarkerColorB = 0x00

# FFT graph limits corners.
upperLeftX_GraphLimit = 18
upperLeftY_GraphLimit = 49
lowerRightX_GraphLimit = 872
lowerRightY_GraphLimit = 530

minX_GraphLimit = upperLeftX_GraphLimit
maxX_GraphLimit = lowerRightX_GraphLimit
minY_GraphLimit = upperLeftY_GraphLimit
maxY_GraphLimit = lowerRightY_GraphLimit

# Search zones.
upperLeftX = 34
upperLeftY = 110
downRightX = 82
downRightY = 157
zone_1 = (upperLeftX, upperLeftY, downRightX, downRightY) 

upperLeftX = 83
upperLeftY = 110
downRightX = 872
downRightY = 530
zone_2 = (upperLeftX, upperLeftY, downRightX, downRightY) 

zoneLst = [zone_1, zone_2] 

######
# Grid

# Grid Y pixel values (pos Y in pixels, attenuation value in dbV, pixel difference from previous):
posY_dBV_table = [ (104, -12.0, 0),
                   (164, -14.0, 60),
                   (224, -16.0, 60),
                   (285, -18.0, 61),
                   (345, -20.0, 60),
                   (405, -22.0, 60),
                   (465, -24.0, 60),
                   (525, -26.0, 60),
                   (585, -28.0, 60)]  # Note: The last data point was added by summing the inter
                                      #       points delta.

delta_dBV = 2.0

dbVOffset = posY_dBV_table[0][1]
min_Y_dBV_limit = (posY_dBV_table[0][0], posY_dBV_table[0][1] - dbVOffset) 
max_Y_dBV_limit = (posY_dBV_table[-1][0], posY_dBV_table[-1][1] - dbVOffset)

# Grid X pixel values (pos X in pixels, frequency in MHz, pixel difference from previous):
bottomLineY = 530
posX_freq_table = [(18,     0.0, 0),
                   (104,  100.0, 86),
                   (190,  200.0, 86),
                   (275,  300.0, 85),
                   (360,  400.0, 85),
                   (445,  500.0, 85),
                   (531,  600.0, 86),
                   (616,  700.0, 85),
                   (701,  800.0, 85),
                   (787,  900.0, 86),
                   (872, 1000.0, 85)]

delta_freq = 100.0

#####################
# Fixed configuration
#####################

pathImgIn    = ".//img_in//"
pathOut      = ".//output_out//"
fileImgOut   = "output_debug_img.png"
CSVFile_dbVAttenuationTable_OriginalFreq = "dbVAttenuationTable_OriginalFreq_0_to_1_GHz.csv"
CSVFile_dbVAttenuationTable_interpolated_1M_Step  = "dbVAttenuationTable_interpol_1M_step_0_to_1_GHz.csv"
CSVFile_dbVAttenuationTable_interpolated_10M_Step = "dbVAttenuationTable_interpol_10M_step_0_to_1_GHz.csv"

# Constants
SHORT_TABLE_MODE = "SHORT_TABLE_MODE"
LONG_TABLE_MODE = "LONG_TABLE_MODE"

longTableHeaderCSV  = ["Frequency MHz", "Attenuation dBV", "VoltsScaleFactor",
                              "Pixel X", "Pixel Y"]
shortTableHeaderCSV = longTableHeaderCSV[ :-2]

###########
# Functions
###########

def getImgInfo(img):
    sizeX = img.size[0]
    sizeY = img.size[1]
    pixels = img.load()   # Create the pixel map
    return (sizeX, sizeY, pixels)

def processZone(pixelsIn, pixelsOut, zone):
    # Extract the pixel points of a zone.
    upperLeftX, upperLeftY, downRightX, downRightY = zone
    pointPairLst = []
    for x in range(upperLeftX, downRightX):
        firstPointY = -1
        counter = 0
        for y in range(upperLeftY, downRightY):
            pix = pixelsIn[x, y]
            r = pix[0]
            g = pix[1]
            b = pix[2]
            if r == signalColorR and g == signalColorG and b == signalColorB:
                if (counter == 0):
                    firstPointY = y
                counter += 1
        if counter > 0:
            calcY = float(firstPointY) + (float(counter - 1) / 2.0)
            pointPairLst.append( [x, calcY] )
            # pixelsOut[x, round(y)] = (outputSignalMarkerColorR,
            #                           outputSignalMarkerColorG,
            #                           outputSignalMarkerColorB)
    return pointPairLst

def startingPointsExtender(pointsPairLst):
    # This function extends the starting points from the first left pixel in "zone 1",
    # flat zone wi 0 dB reference attenuation all the way to the zero frequency (0 Hz),
    # starting graph X position.
    startGraphPosX = minX_GraphLimit + 1
    firstPoint = pointsPairLst[0]
    endValueX, valueY = firstPoint
    for x in range(endValueX, startGraphPosX, -1):
        pointsPairLst.insert(0, [x, valueY])
    return pointsPairLst

def extractSignalPixelPos(pixelsIn, pixelsOut, zoneLst):
    # Extract the FFT line plot pixel positions of the PNG image.
    lstPointPairs = []
    for zone in zoneLst:
        zonePoints = processZone(pixelsIn, pixelsOut, zone)
        lstPointPairs += zonePoints 
    return lstPointPairs

def markPointsInOutputImg(pointsPairLst, pixelsOut):
    # Add the marking over a copy of the input image for verification
    # of correctness, rapid validation to help in development.

    # Plot the 4 corners graph limits.
    if flag_mark_4_corners_graph_limits == True:
        points = [(minX_GraphLimit, minY_GraphLimit),
                  (minX_GraphLimit, maxY_GraphLimit),
                  (maxX_GraphLimit, minY_GraphLimit),
                  (maxX_GraphLimit, maxY_GraphLimit)]     
        for x, y in points:
            pixelsOut[x, round(y)] = (outputSignalMarkerColorR,
                                      outputSignalMarkerColorG,
                                      outputSignalMarkerColorB)
    
    # Plot or mark the extracted signal points.
    if flag_plot_extracted_signal_points == True:
        firstZone = 0
        zone_0_lowerX, _, _ , _ = zoneLst[firstZone]
        for pointsPair in  pointsPairLst:
            x, y = pointsPair
            if x < zone_0_lowerX:
                # Plot extension in Red color.
                pixelsOut[x, round(y)] = (outputSignalMarkerInitialExtensionColorR,
                                          outputSignalMarkerInitialExtensionColorG,
                                          outputSignalMarkerInitialExtensionColorB)
            else:
                # Plot normal signal in White color.
                pixelsOut[x, round(y)] = (outputSignalMarkerColorR,
                                          outputSignalMarkerColorG,
                                          outputSignalMarkerColorB)

    # Mark the left grid Y points.
    if flag_mark_left_grid_Y_points == True:
        x = minX_GraphLimit 
        for val in posY_dBV_table:
            y, dbV, pixelDiff_Y = val
            pixelsOut[x, y] = (outputGrid_Y_MarkerColorR,
                               outputGrid_Y_MarkerColorG,
                               outputGrid_Y_MarkerColorB)

    # Mark the bottom grid X points.
    if flag_mark_bottom_grid_X_points == True:
        y = maxY_GraphLimit
        for val in posX_freq_table:
            x, freq, pixelDiff_X = val
            pixelsOut[x, y] = (outputGrid_X_MarkerColorR,
                               outputGrid_X_MarkerColorG,
                               outputGrid_X_MarkerColorB)

def calculateVoltfactor(dBV):
    # 1 V = 0 dBv.
    #
    # The formula for Volts to dBv conversion is:
    #
    # dBV = 20 * log10( Volts )
    #
    # reverse formula for converting dBv to Volts is:
    #
    # Volts = 10 ^ ( dBV/20 )

    voltScaleFactor = math.pow(10.0, dBV / 20.0)
    return voltScaleFactor

def mapToFreq_and_dB(pointsPairLst, pixelsOut):
    flag_function_debug = True

    mappedOutPutPointsPairLst = []
    dB_zero_point = pointsPairLst[zoneLst[0][0] - minX_GraphLimit + 1] 
    pos_Y_zero_dBV_ref = dB_zero_point[1]
    print("pos_Y_zero_dBV_ref: ", str(pos_Y_zero_dBV_ref), 
          " -->  dBV: 0.0  Volts scale factor: 1.0")
    if flag_function_debug == True:
        r = 0x00
        b = 0x00
        g = 0xFF
        pixelsOut[dB_zero_point[0], pos_Y_zero_dBV_ref] = (r, g, b)
    for point in pointsPairLst:
        x, y = point
        freq = (float(x - minX_GraphLimit) / float(maxX_GraphLimit - minX_GraphLimit) ) * 1000.0
        dBV = (float(y - pos_Y_zero_dBV_ref ) / float(max_Y_dBV_limit[0] - min_Y_dBV_limit[0]) ) * ( max_Y_dBV_limit[1] - min_Y_dBV_limit[1] )
        voltScaleFactor = calculateVoltfactor(dBV)
        tupleVal = [freq, dBV, voltScaleFactor, x, y]
        mappedOutPutPointsPairLst.append(tupleVal)
        # Print values
        # if 480 < freq < 600:
        #    print(tupleVal) 
    return mappedOutPutPointsPairLst

def getInterpolated_dB_for_freq(mappedPointsPairLst, freq, flag_print):
    # Note: 
    # -3.01dBV = 0.7071 Volts  

    xFreqPoints = np.array([point[0] for point in mappedPointsPairLst])
    y_dBV_Points = np.array([point[1] for point in mappedPointsPairLst])
    # We use the interpolation in dBV and then calculate the Volts scale factor.  
    # y_VoltsScaleFactor_Points = np.array([calculateVoltfactor(point[1]) for
    #                                      point in mappedPointsPairLst])
    
    # y_VoltsScaleFactor_Points = np.array([point[2] for point in mappedPointsPairLst])

    # Perform the interpolation.
    interp_dBV         = np.interp(freq, xFreqPoints, y_dBV_Points)
    interp_voltsFactor = calculateVoltfactor(interp_dBV)
    #interp_voltsFactor = np.interp(freq, xFreqPoints, y_VoltsScaleFactor_Points)
    if flag_print == True:
        print("freq:", str(freq), "  dBV:", str("%.4f" % interp_dBV), "  Volts scale factor:",
              str("%.4f" % interp_voltsFactor))
    return (freq, interp_dBV, interp_voltsFactor)

def readFromCSVFile(inputPath, fileName):
    headerRow = None
    outputTable = []
    with open(inputPath + fileName, mode='r', newline='') as csvFile:
        tableReader = csv.reader(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        flag_first_row = True
        for row in tableReader:
            if flag_first_row == True:
                # Reading the header. 
                headerRow = row
                flag_first_row = False
            else:
                # Reading the data rows.    
                outputTable.append(row)
            print(', '.join(row))      
    return (headerRow, outputTable)

def writeToCSVFile(mappedPointsPairLst, pathOut, fileName, tableMode):
    with open(pathOut + fileName, mode='w', newline='') as tableFile:
        tableWriter = csv.writer(tableFile, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL )
        # Writing the header.
        if tableMode == SHORT_TABLE_MODE:
            tableWriter.writerow(shortTableHeaderCSV)
        elif tableMode == LONG_TABLE_MODE:
            tableWriter.writerow(longTableHeaderCSV)
        # Writing the rows.
        for point in mappedPointsPairLst:
            tableWriter.writerow(point)
            # freq, dBV, voltsScaleFactor, x, y = point
            # tableWriter.writerow([freq, dBV, voltsScaleFactor, x, y])

def calcFixedStepInterpolAttenuationTable(mappedPointsPairLst, freqStep,
                                          freqRange, flag_print):
    # Param: freqRange is a tuple "(startFreq, endFreq)".
    if flag_print == True:
        print("")  # Just to add a "\n". 
    fixedStepTable = []
    startFreq = freqRange[0]
    endFreq   = freqRange[1]
    numIntervals = int((endFreq - startFreq + freqStep) / freqStep)

    # Extend the range from 0Hz up to 1000MHz, so that interpolation work well.
    tmpPointsPairLst = mappedPointsPairLst.copy()
    # Insert synthetic 0 MHz with 0.0 dBV value in the begining.
    tmpIndex = 0
    tmpFreq  = 0.0
    tmp_dBV  = 0.0
    tmpPointsPairLst.insert(tmpIndex, [tmpFreq, tmp_dBV])
    # Append to the end 1 synthetic data point, 1 MHz past the last real value with -100 dBV.
    lastIndex = len(tmpPointsPairLst) - 1
    tmpFreq   = tmpPointsPairLst[lastIndex][0] + 1.0 # MHz
    tmp_dBV   = -100.0
    tmpPointsPairLst.append([tmpFreq, tmp_dBV])
    # Append to the end 1 synthetic data point at 1 GHz with -100 dBV.
    tmpFreq = 1000 # MHz
    tmp_dBV = -100.0
    tmpPointsPairLst.append([tmpFreq, tmp_dBV])

    for intervalIndex in range(0, numIntervals):
        freq = startFreq + freqStep * intervalIndex
        dataPoint = getInterpolated_dB_for_freq(tmpPointsPairLst, freq, flag_print)
        fixedStepTable.append(dataPoint)
    if flag_print == True:
        print("")  # Just to add a "\n". 
    return fixedStepTable

######
# Main
######

if __name__ == "__main__":
    # Load the scope PNG image from file.
    print("\nStarting...")
    imgIn = Image.open(pathImgIn + fileImgIn)
    print("...input scope PNG image loaded...\n")
    imgOut = imgIn.copy()

    # Image In and Out info. 
    sizeInX, sizeInY, pixelsIn = getImgInfo(imgIn)
    sizeOutX, sizeOutY, pixelsOut = getImgInfo(imgOut)
    
    pointsPairLst = extractSignalPixelPos(pixelsIn, pixelsOut, zoneLst)
    pointsPairLst = startingPointsExtender(pointsPairLst)
    markPointsInOutputImg(pointsPairLst, pixelsOut)
    mappedPointsPairLst = mapToFreq_and_dB(pointsPairLst, pixelsOut)

    flag_print = True
    freq = 430.0  # MHz
    val_3dBV = getInterpolated_dB_for_freq(mappedPointsPairLst, freq, flag_print)
    
    freq = 500.0  # MHz
    val_3dBV = getInterpolated_dB_for_freq(mappedPointsPairLst, freq, flag_print)

    freq = 570.0  # MHz
    val_3dBV = getInterpolated_dB_for_freq(mappedPointsPairLst, freq, flag_print)

    print("")
    writeToCSVFile(mappedPointsPairLst, pathOut,
                   CSVFile_dbVAttenuationTable_OriginalFreq, LONG_TABLE_MODE)
    print("...output CSV graph original freq. attenuation file generated...")

    # Note: Uncomment to test the reading of the file. 
    # CSVFromFiletable = readFromCSVFile( pathOut, CSVFile_dbVAttenuationTable_OriginalFreq)
    # print(CSVFromFiletable)

    freqStep = 10.0 # MHz
    freqRange = (0.0, 1000.0) # MHz
    flag_print = False
    fixedStep_10M_attTable = calcFixedStepInterpolAttenuationTable(mappedPointsPairLst,
                                                                   freqStep, freqRange, flag_print)
    writeToCSVFile(fixedStep_10M_attTable, pathOut,
                   CSVFile_dbVAttenuationTable_interpolated_10M_Step, SHORT_TABLE_MODE)
    print("...output CSV 10 MHz step interpolated attenuation (0 Hz to 1GHz) file generated...")


    freqStep = 1.0 # MHz
    freqRange = (0.0, 1000.0) # MHz
    flag_print = False
    fixedStep_1M_attTable = calcFixedStepInterpolAttenuationTable(mappedPointsPairLst,
                                                                  freqStep, freqRange, flag_print)
    writeToCSVFile(fixedStep_1M_attTable, pathOut,
                   CSVFile_dbVAttenuationTable_interpolated_1M_Step, SHORT_TABLE_MODE)
    print("...output CSV  1 MHz step interpolated attenuation (0 Hz to 1GHz) file generated...")

    # Write the debug extrated points validaion of the scope processed output PNG image. 
    imgOut.save(pathOut + fileImgOut)
    print("...output extracted points validation scope processed PNG image file generated...")

    print("...end\n")



