##
# Homework 03
# Ben Buckley
# CIS-2212
# Fall, 2021
#

from sqlalchemy import create_engine    #Magic to connect with a SQL DB
from datetime import datetime           #Structured date objects
import pyodbc       #Is this actually doing anything?  Highlighting has it grey...
import numpy as np  #For trigonometric functions compatible with DataFrame.apply()
import pandas as pd #Pandas DataFrames to manipulate tabular data
import math         #For pi

#Suppress chain assigment warnings.
#from https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
pd.options.mode.chained_assignment = None  # default='warn'

##
# Function Definitions

def julianDate(date):
    ##
    # Translation of:
    '''
    -- Compute the Julian day number for 0h UTC on the Gregorian date given.
    CREATE FUNCTION JulianDay(
            @Y integer, @M integer, @D integer) RETURNS float AS
    BEGIN
    DECLARE @Year  integer = @Y;
    DECLARE @Month integer = @M;
    DECLARE @Day   integer = @D;
    DECLARE @A     integer;
    DECLARE @B     integer;

    IF @Month <= 2
        BEGIN
        SET @Year = @Year - 1;
        SET @Month = @Month + 12;
        END;
    SET @A = @Year/100;
    SET @B = 2 - @A + (@A/4);
    RETURN floor(365.25 * (@Year + 4716)) + floor(30.6001 * (@Month + 1)) + @Day + @B - 1524.5;
    END;
    GO
    '''

    if (date.month <= 2):
        date.year -= 1
        date.month += 12
    A = date.year//100
    B = 2 - A + (A//4)
    year = int(365.25 * (date.year + 4716)) + int(30.6001 * (date.month + 1)) + (date.day + B - 1524.5)
    return year

def siderealTime(date):
    ##
    # Translation of:
    '''
    -- Compute the sidereal time at the prime meridian for the date/time given. The return value is
    -- given in degrees (24 hours = 360 degrees).
    CREATE FUNCTION SiderealTime(
            @Year integer, @Month  integer, @Day    integer,
            @Hour integer, @Minute integer, @Second integer) RETURNS float AS
    BEGIN
    DECLARE @T       float;
    DECLARE @Theta_0 float;
    DECLARE @Theta   float;

    SET @T = (dbo.JulianDay(@Year, @Month, @Day) - 2451545.0)/36525.0;
    SET @Theta_0 = 100.46061837 + 36000.770053608*@T + 0.000387933*@T*@T + (@T*@T*@T)/38710000.0;
    SET @Theta = 1.00273790935*360.0*((@Second + 60.0*(@Minute + 60.0*@Hour))/86400);
    SET @Theta = @Theta + @Theta_0;
    WHILE @Theta > 360.0
        BEGIN
        SET @Theta = @Theta - 360.0;
        END;
    RETURN @Theta;
    END;
    GO
    '''
    t = (julianDate(date) - 2451545.0)/36525.0
    theta_0 = 100.46061837 + (36000.770053608 * t) + (0.000387933 * t * t) + ((t * t * t)/38710000.0)
    theta = (1.00273790935 * 360.0 * ((date.second + (60 * (date.minute + (60.0 * date.hour)))))) / 86400
    theta += theta_0

    theta = theta % 360.0
    return theta

def siderealLocalTime(date,longitude):
    ##
    # Translation of:
    '''
    CREATE FUNCTION LocalSiderealTime(
            @Year  integer, @Month  integer, @Day    integer,
            @Hour  integer, @Minute integer, @Second integer,
            @Longitude float) returns float AS
    BEGIN
    DECLARE @Prime_Time float = dbo.SiderealTime(@Year, @Month, @Day, @Hour, @Minute, @Second);
    RETURN @Prime_Time + @Longitude;
    END;
    GO
    '''

    primeTime = siderealTime(date)
    local = primeTime + longitude
    return local

def printDataFrame(df):
    ##
    #  A general routine to iterate over a DataFrame row-wise and print
    #   it's values in a nice table with column values as headers
    #
    #   First print tab-separated column names
    #   Print the values of each subsequent row tab-separated
    #   Reprint the column names every headerRepeat rows (or never, by default)

    for item in df.iterrows():

        index, row = item     # 'item' is a pair. Split it into components.
        
        if (index == 0):
            # On the first item, print the column names
            
            for column in df.columns.values:
                #Center 'column" in a 15 char field followed by a tab
                print('{:^15}'.format(column),end="\t")
            print()

        else:
            # Print values in each row

            for column in df.columns.values:
                #Right justify 'row[colum]' in 15 chars plus a tab
                print('{:>15}'.format(row[column]),end="\t")
            print()

##
# Main Body

#Take user input; provide defaults to speed up testing
constName = input("Please enter the constellation short name (i.e.: Ori, Aur, CMa, etc.) [Cas] --> ") or "Cas"
gpsInput = input("Please enter your GPS coords, comma-separated [VTC] -->").split(',') or [43.93889466870274,-72.60474245975041]
gpsInput = list(map(float,gpsInput))
gpsCoords = {'lat':gpsInput[0],'long':gpsInput[1]}

now = str(datetime.now())   # Snapshot of the current day and time in a string
now = now[:now.rfind(':')]  # Chop off seconds and useconds by slicing at the last ':'
# This gives us the current moment in a string that matches the strptime()
# format below.  Ironically, I do absolutely no validation of the user's
# input after all this work to get a viable default value *shrug
dateString = input("Enter date and time (yyyy-mm-dd hh:mm) [NOW] --> ") or now
date = datetime.strptime(dateString,"%Y-%m-%d %H:%M")

# Create an "engine" for accessing the DBMS using an appropriate connection string.
engine = create_engine("mssql+pyodbc://student:2frenchfry!@VariableStars")
connection = engine.connect()

# Now use Pandas to issue an SQL query to the DBMS and retrieve the resuls as a DataFrame.
# This query selects visible stars from the named constellation
sqlCommand = "SELECT name, const, ra, dec, max_bright, min_bright FROM star"
sqlCondition = "WHERE const = '"+constName+"' and min_bright >= 1.0 and min_bright <= 10.0;"
visibleStarsByConstellation = pd.read_sql(sqlCommand+" "+sqlCondition, connection)
connection.close()  # Clean-up

# Create a working DataFrame with the name, right ascension and declination of the visible stars
starAltitudes = visibleStarsByConstellation[["name","ra","dec"]]

# Calculate the Pole Zenith (in radians) and its Sin and Cos
starAltitudes["poleZenith"] = ((90.0 - gpsCoords['lat']) / 360.0) * 2 * math.pi
starAltitudes["poleZenithSin"] = starAltitudes["poleZenith"].apply(np.sin)
starAltitudes["poleZenithCos"] = starAltitudes["poleZenith"].apply(np.cos)

# Calculate the Pole Star (in radians) and its Sin and Cos
starAltitudes["poleStar"] = ((90.0 - starAltitudes["dec"]) / 360.0) * 2 * math.pi
starAltitudes["poleStarSin"] = starAltitudes["poleStar"].apply(np.sin)
starAltitudes["poleStarCos"] = starAltitudes["poleStar"].apply(np.cos)

# Calculate the difference between right ascension and the local sidereal time (in radians),
# and its Cos
siderealLocal = siderealLocalTime(date,gpsCoords['long'])
starAltitudes["raDiff"] = ((starAltitudes["ra"] - siderealLocal) / 360.0) * 2 * math.pi
starAltitudes["raDiffCos"] = starAltitudes["raDiff"].apply(np.cos)

#Calculate the stars' zeniths and convert back to degrees
starAltitudes["zenithStar"] = ( 
        (starAltitudes["poleZenithCos"] * starAltitudes["poleStarCos"]) +
        (starAltitudes["poleZenithSin"] * starAltitudes["poleStarSin"] * starAltitudes["raDiffCos"])
    ).apply(np.arccos)
starAltitudes["zenithStar"] = 360.0 * (starAltitudes["zenithStar"] / (2 * math.pi))

#Calculate the stars' altitudes
starAltitudes["altitude"] = 90.0 - starAltitudes["zenithStar"]

#Create a final DataFrame with name, const, and altitude
final = pd.merge(visibleStarsByConstellation[["name","ra","dec"]],starAltitudes[["name","altitude"]],how="left",on="name")

print("The visible stars in ",constName,
    " and their altitudes from {:.5f}".format(gpsCoords['lat']),", {:.5f}".format(gpsCoords['long']),
    " on {}/{}, {}".format(date.month,date.day,date.year)," at ",date.time(),":",sep="")
printDataFrame(final)

##
# DEBUG TEST PRINTS
#
#print("\nNumber of elements in 'final' is ",final.size)
#print("The number of rows in 'final' is ",final.shape[0])
#print("The number of cols in 'final' is ",final.shape[1])
#print("The columns are ",final.columns.values)
#print("GPS coordinates are: ",gpsLat,", ",gpsLong)
#print("The date and time is: ",date)
#print("The Julian Date is: ",julian)
#print("Sideral Time :",sidereal)
#print("Local Sidereal time: ",siderealLocal)