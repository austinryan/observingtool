# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import math
import sys


#------------------------USER INPUTTED VALUES-------------------------------

latitude = 40.993 #degrees north of equater (negative if using south)
longitude = 99.0817 #degrees west of greenwhich (negative if using east)
N = 215 #day of the year, example: august 3rd = 215
UT_offset = -5 #example: Central Time Zone (no daylight savings) is UT -6, therefore you would put the value -6 here. easily googled.
RA_hours = 18. #RA hour
RA_minutes = 36. #RA  minutes
RA_seconds = 56 #RA seconds
DEC_degrees = 89. #DEC degrees
DEC_minutes = 47. #DEC minutes
DEC_seconds = 1. #DEC seconds

#below here you can query altitude and air mass at a specified time

query_local_hours = 8. #use military time in YOUR time zone. useful for getting air masses at specific times like astronomical twilight
query_local_minutes = 37. #use military time

#-----------------------CODE BELOW DO NOT CHANGE-----------------------------

alt = 0

#CALCULATE: RA AND DEC IN DEGREES
RA = ((15*RA_hours)+(15*RA_minutes/60)+(15*RA_seconds/3600))
DEC = (DEC_degrees + DEC_minutes/60 + DEC_seconds/3600)

#convert query local times to query UT
query_UT_hours = query_local_hours - UT_offset
if query_UT_hours > 24:
    query_UT_hours = query_UT_hours - 24.
if query_UT_hours < 0:
    query_UT_hours = query_UT_hours + 24.
query_UT_minutes = query_local_minutes

#CALCULATE: Zenith local time calculation (valid for all stars in the sky even if they dont rise or set)
Zenith_time_LST = RA
Zenith_time_LST_hours = Zenith_time_LST/15
Zenith_time_LST_minutes = (Zenith_time_LST_hours-int(Zenith_time_LST_hours))*60
Zenith_time_GMST_hours = Zenith_time_LST_hours + (longitude/15.)
if Zenith_time_GMST_hours < 0:
    Zenith_time_GMST_hours = 24. + Zenith_time_GMST_hours
if Zenith_time_GMST_hours >= 24:
    Zenith_time_GMST_hours = Zenith_time_GMST_hours - 24.
Zenith_time_UT_hours = (Zenith_time_GMST_hours - 6.656306 - (0.0657098242 * (N)))/1.0027379093
if Zenith_time_UT_hours < 0:
    Zenith_time_UT_hours = Zenith_time_UT_hours + 24.
if Zenith_time_UT_hours >= 24:
    Zenith_time_UT_hours = Zenith_time_UT_hours - 24.
Zenith_time_local_hours = Zenith_time_UT_hours + UT_offset
if Zenith_time_local_hours < 0:
    Zenith_time_local_hours = Zenith_time_local_hours + 24.
if Zenith_time_local_hours >= 24:
    Zenith_time_local_hours = Zenith_time_local_hours - 24.
Zenith_time_local_minutes = (Zenith_time_local_hours-int(Zenith_time_local_hours))*60.


#CALCULATE: altitude at Zenith, air mass at Zenith, h=0 at Zenith.
alt_Zenith = (180./math.pi)*(math.asin((math.sin(math.radians(latitude))*math.sin(math.radians(DEC)))+(math.cos(math.radians(latitude))*math.cos(math.radians(DEC)))))
z_Zenith = 90-alt_Zenith
air_mass_Zenith = (1/math.cos(math.radians(z_Zenith)))

#Convert query UT -> GMST -> LST then calculate hour angle.
GMST_query = 6.656306 + (0.0657098242 * N) + (1.0027379093*(query_UT_hours+(query_UT_minutes/60)))
if GMST_query >= 24:
    GMST_query = GMST_query - 24.
if GMST_query < 0:
    GMST_query = GMST_query + 24.
LST_query = GMST_query - (longitude/15)
if LST_query >= 24:
    LST_query = LST_query - 24.
if LST_query < 0:
    LST_query = LST_query + 24.
h_query = LST_query - (RA/15.)
if h_query >= 24:
    h_query = h_query - 24.
if h_query < 0:
    h_query = h_query + 24.
h_query_degrees = h_query * 15

#Calculate altitude at query and air mass at query
alt_query = (180/math.pi)*(math.asin((math.sin(math.radians(latitude))*math.sin(math.radians(DEC)))+(math.cos(math.radians(latitude))*math.cos(math.radians(DEC))*math.cos(math.radians(h_query_degrees)))))
z_query = 90-alt_query
air_mass_query = (1/math.cos(math.radians(z_query)))

#CHECK IF THE OBJECT SETS OR RISES
cosh=(-math.tan(math.radians(latitude))*math.tan(math.radians(DEC)))
#IF CASE FOR OBJECT NEVER SETTING
if cosh < -1: #object never sets
    print"The object at your latitude will never set!"
    print"------------------------------------"
    print"Zenith time for your object in military time is",int(Zenith_time_local_hours),"ʰ",int(Zenith_time_local_minutes),"ᵐ"
    print"------------------------------------"
    if int(Zenith_time_local_hours) == 0:
        AM_PM_Zenith_hours = Zenith_time_local_hours + 12
        print"Zenith time for your object in local time is",int(AM_PM_Zenith_hours),":",int(Zenith_time_local_minutes),"am"
    if 1 <= int(Zenith_time_local_hours) < 12:
        AM_PM_Zenith_hours = Zenith_time_local_hours
        print"Zenith time for your object in local time is",int(AM_PM_Zenith_hours),":",int(Zenith_time_local_minutes),"am"
    if int(Zenith_time_local_hours) == 12:
        AM_PM_Zenith_hours = Zenith_time_local_hours
        print"Zenith time for your object in local time is",int(AM_PM_Zenith_hours),":",int(Zenith_time_local_minutes),"pm"
    if int(Zenith_time_local_hours) >= 13:
        AM_PM_Zenith_hours = Zenith_time_local_hours - 12
        print"Zenith time for your object in local time is",int(AM_PM_Zenith_hours),":",int(Zenith_time_local_minutes),"pm"
    print"------------------------------------"
    print"Altitude at Zenith is",alt_Zenith,"degrees"
    print"Air mass at Zenith is",air_mass_Zenith
    print"------------------------------------"
    
    #Print altitude and air mass at query time"
    print"Altitude at query time is",alt_query,"degrees"
    print"Air mass at query time is",air_mass_query
    print"------------------------------------"
    sys.exit()
    
#IF CASE FOR OBJECT NEVER RISING
if cosh > 1:
    print"The object at your latitude will never be in the sky"
    sys.exit()
    
#IF CASE FOR OBJECT RISING AND SETTING
if -1 <= cosh <= 1:
    
    #calculate hour angle in degrees   
    h = (180./math.pi)*math.acos(cosh)

    #calculate rise and set times in degrees
    rise_time_LST = RA - h
    set_time_LST = RA + h
    if rise_time_LST < 0:
        rise_time_LST = 360. + rise_time_LST
    if set_time_LST < 0:
        set_time_LST = 360. + set_time_LST
    if rise_time_LST >= 360:
        rise_time_LST = rise_time_LST - 360.
    if set_time_LST >= 360:
        set_time_LST = set_time_LST - 360.

    #CONVERT RISE AND SET TIMES FROM DEGREES TO HOURS AND MINUTES
    set_time_LST_hours = set_time_LST/15.
    set_time_LST_minutes = (set_time_LST_hours-int(set_time_LST_hours))*60.

    rise_time_LST_hours = rise_time_LST/15.
    rise_time_LST_minutes = (rise_time_LST_hours-int(rise_time_LST_hours))*60.
    
    #Calculate the GMST in hours (Zenith time for example)
    rise_time_GMST_hours = rise_time_LST_hours + (longitude/15.)
    set_time_GMST_hours = set_time_LST_hours + (longitude/15.)
    if rise_time_GMST_hours < 0:
        rise_time_GMST_hours = 24. + rise_time_GMST_hours
    if rise_time_GMST_hours >= 24:
        rise_time_GMST_hours = rise_time_GMST_hours - 24.
    if set_time_GMST_hours < 0:
        set_time_GMST_hours = 24. + set_time_GMST_hours
    if set_time_GMST_hours >= 24:
        set_time_GMST_hours = set_time_GMST_hours - 24.
    
    #calculate UT military time
    rise_time_UT_hours = (rise_time_GMST_hours - 6.656306 - (0.0657098242 * (N)))/1.0027379093
    set_time_UT_hours = (set_time_GMST_hours - 6.656306 - (0.0657098242 * (N)))/1.0027379093
    if rise_time_UT_hours < 0:
        rise_time_UT_hours = rise_time_UT_hours + 24
    if rise_time_UT_hours >= 24:
        rise_time_UT_hours = rise_time_UT_hours - 24.
    if set_time_UT_hours < 0:
        set_time_UT_hours = set_time_UT_hours + 24
    if set_time_UT_hours >= 24:
        set_time_UT_hours = set_time_UT_hours - 24.
    
    #find local military time from UT military time
    rise_time_local_hours = rise_time_UT_hours + UT_offset
    set_time_local_hours = set_time_UT_hours + UT_offset
    if rise_time_local_hours < 0:
        rise_time_local_hours = rise_time_local_hours + 24
    if rise_time_UT_hours >= 24:
        rise_time_local_hours = rise_time_local_hours - 24.
    if set_time_local_hours < 0:
        set_time_local_hours = set_time_local_hours + 24
    if rise_time_UT_hours >= 24:
        set_time_local_hours = set_time_local_hours - 24.
    
    #convert the hour decimals into minutes
    rise_time_local_minutes = (rise_time_local_hours-int(rise_time_local_hours))*60.
    set_time_local_minutes = (set_time_local_hours-int(set_time_local_hours))*60.
    
    #print local military times
    print"Local Military Time:"
    if rise_time_local_minutes < 10:
        print"Rise time for your object is",str(int(rise_time_local_hours))+"ʰ",'0'+str(int(rise_time_local_minutes))+"ᵐ"
    else:
        print"Rise time for your object is",str(int(rise_time_local_hours))+"ʰ",str(int(rise_time_local_minutes))+"ᵐ"
    if Zenith_time_local_minutes < 10:
        print"Zenith time for your object is:",str(int(Zenith_time_local_hours))+"ʰ",'0'+str(int(Zenith_time_local_minutes))+"ᵐ"
    else:   
        print"Zenith time for your object is",str(int(Zenith_time_local_hours))+"ʰ",str(int(Zenith_time_local_minutes))+"ᵐ"
    if set_time_local_minutes < 10:
        print"Set time in for your object is",str(int(set_time_local_hours))+"ʰ","0"+str(int(set_time_local_minutes))+"ᵐ"
    else:
        print"Set time in for your object is",str(int(set_time_local_hours))+"ʰ",str(int(set_time_local_minutes))+"ᵐ"
    print"---------------------------------------"
    
    #calculate and print local clock times
    
    #check for less than 10 minutes, then add a leading zero
    
    if rise_time_local_minutes < 10:
        rise_time_local_minutes = '0'+str(int(rise_time_local_minutes))
    else:
        rise_time_local_minutes = str(int(rise_time_local_minutes))
    if Zenith_time_local_minutes < 10:
        Zenith_time_local_minutes = '0'+str(int(Zenith_time_local_minutes))
    else:
        Zenith_time_local_minutes = str(int(Zenith_time_local_minutes))
    if set_time_local_minutes < 10:
        set_time_local_minutes = '0'+str(int(set_time_local_minutes))
    else:
        set_time_local_minutes = str(int(set_time_local_minutes))
        
    print"Local Clock Time:"
    if int(rise_time_local_hours) == 0:
        AM_PM_rise_hours = rise_time_local_hours + 12
        print"Rise time for your object is",str(int(AM_PM_rise_hours))+":"+(rise_time_local_minutes),"am"
    if 1 <= int(rise_time_local_hours) < 12:
        AM_PM_rise_hours = rise_time_local_hours
        print"Rise time for your object is",str(int(AM_PM_rise_hours))+":"+(rise_time_local_minutes),"am"
    if int(rise_time_local_hours) == 12:
        AM_PM_rise_hours = rise_time_local_hours
        print"Rise time for your object is",str(int(AM_PM_rise_hours))+":"+(rise_time_local_minutes),"pm"
    if int(rise_time_local_hours) >= 13:
        AM_PM_rise_hours = rise_time_local_hours - 12
        print"Rise time for your object is",str(int(AM_PM_rise_hours))+":"+(rise_time_local_minutes),"pm"
    
    if int(Zenith_time_local_hours) == 0:
        AM_PM_Zenith_hours = Zenith_time_local_hours + 12
        print"Zenith time for your object is",str(int(AM_PM_Zenith_hours))+":"+(Zenith_time_local_minutes),"am"
    if 1 <= int(Zenith_time_local_hours) < 12:
        AM_PM_Zenith_hours = Zenith_time_local_hours
        print"Zenith time for your object is",str(int(AM_PM_Zenith_hours))+":"+(Zenith_time_local_minutes),"am"
    if int(Zenith_time_local_hours) == 12:
        AM_PM_Zenith_hours = Zenith_time_local_hours
        print"Zenith time for your object is",str(int(AM_PM_Zenith_hours))+":"+(Zenith_time_local_minutes),"pm"
    if int(Zenith_time_local_hours) >= 13:
        AM_PM_Zenith_hours = Zenith_time_local_hours - 12
        print"Zenith time for your object is",str(int(AM_PM_Zenith_hours))+":"+(Zenith_time_local_minutes),"pm"
        
    if int(set_time_local_hours) == 0:
        AM_PM_set_hours = set_time_local_hours + 12
        print"Set time for your object is",str(int(AM_PM_set_hours))+":"+(set_time_local_minutes),"am"
    if 1 <= int(set_time_local_hours) < 12:
        AM_PM_set_hours = set_time_local_hours
        print"Set time for your object is",str(int(AM_PM_set_hours))+":"+(set_time_local_minutes),"am"
    if int(set_time_local_hours) == 12:
        AM_PM_set_hours = set_time_local_hours
        print"Set time for your object is",str(int(AM_PM_set_hours))+":"+(set_time_local_minutes),"pm"
    if int(set_time_local_hours) >= 13:
        AM_PM_set_hours = set_time_local_hours - 12
        print"Set time for your object is",str(int(AM_PM_set_hours))+":"+(set_time_local_minutes),"pm"
    
    print"------------------------------------"
    
    print"Altitude at Zenith is",alt_Zenith,"degrees"
    print"Air mass at Zenith is",air_mass_Zenith
    
    print"------------------------------------"
    
    #Print altitude and air mass at query time"
    print"Altitude at query time is",alt_query,"degrees"
    print"Air mass at query time is",air_mass_query
    print"------------------------------------"
        
    
    
    
    

