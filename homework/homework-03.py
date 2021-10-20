from sqlalchemy import create_engine
from datetime import datetime
import pyodbc
import pandas as pd

constName = input("Please enter the constellation short name (i.e.: Ori, Aur, CMa, etc.) --> ") or "Cas"
gpsLat,gpsLong = input("Please enter your GPS coords, comma-separated -->") or 43.93889466870274,-72.60474245975041

now = str(datetime.now())   # Snapshot of the current day and time in a string
now = now[:now.rfind(':')]  # Chop off seconds and useconds by slicing at the last ':'
# This gives us the current moment in a string that matches the strptime()
# format below.  Ironically, I do absolutely no validation of the user's
# input after all this work to get a viable default value *shrug*
dateString = input("Enter date and time (yyyy-mm-dd hh:mm) --> ") or now
date = datetime.strptime(dateString,"%Y-%m-%d %H:%M") 

# Create an "engine" for accessing the DBMS using an appropriate connection string.
engine = create_engine("mssql+pyodbc://student:2frenchfry!@VariableStars")
connection = engine.connect()

# Now use a Pandas to issue an SQL query to the DBMS and retrieve the resuls as a DataFrame.
sqlCommand = "SELECT name, const, ra, dec, max_bright, min_bright FROM star"
sqlCondition = "WHERE const = '"+constName+"' and min_bright >= 1.0 and min_bright <= 10.0;"
visibleStarsByConstellation = pd.read_sql(sqlCommand+" "+sqlCondition, connection)
connection.close()

# Now use Pandas to manipulate the data we retrieved.
#orion_stars["brightness_difference"] = orion_stars["min_bright"] - orion_stars["max_bright"]
#columns = ["name", "const", "ra", "dec", "max_bright", "min_bright"]
#orion_wide = orion_stars.loc[orion_stars["brightness_difference"] >= 1, columns]
#observable = orion_wide[orion_wide["min_bright"] <= 10.0]

#Create a final DataFrame for output and print it
final = visibleStarsByConstellation

print("Rows of 'final':")
for item in final.iterrows():
    index, row = item     # 'item' is a pair. Split it into components.
    print("\nRow #: ",index)
    for column in final.columns.values:
        print(column,": ",row[column])

print("\nNumber of elements in 'final' is ",final.size)
print("The number of rows in 'final' is ",final.shape[0])
print("The number of cols in 'final' is ",final.shape[1])
print("The columns are ",final.columns.values)
print("\nGPS coordinates are: ",gpsLat,", ",gpsLong)
print("\nThe date and time is: ",date)