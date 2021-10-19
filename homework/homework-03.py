from sqlalchemy import create_engine
from datetime import datetime
import pyodbc
import pandas as pd

constName = "Cas"
#constName = input("Please enter the constellation short name (i.e.: Ori, Aur, CMa, etc.) --> ")
gpsLat,gpsLong = 43.93889466870274,-72.60474245975041
#gpsLat,gpsLong = input("Please enter your GPS coords, comma-separated -->")
date = datetime.today()
#dateString = str(input("Enter date and time(yyyy-mm-dd hh:mm) --> ""))
#date = datetime.strptime(dateString, "%Y-%m-%d %H:%M")

# Create an "engine" for accessing the DBMS using an appropriate connection string.
engine = create_engine("mssql+pyodbc://student:2frenchfry!@VariableStars")
connection = engine.connect()

# Now use a Pandas to issue an SQL query to the DBMS and retrieve the resuls as a DataFrame.
#sql_string = "SELECT name, const, max_bright, min_bright FROM star WHERE const = 'Ori'"
sql_command = "SELECT name, const, ra, dec, max_bright, min_bright FROM star"
sql_conditions = "WHERE const = '"+constName+"' and min_bright >= 1.0 and min_bright <= 10.0;"
orion_stars = pd.read_sql(sql_command+" "+sql_conditions, connection)
connection.close()

# Now use Pandas to manipulate the data we retrieved.
#orion_stars["brightness_difference"] = orion_stars["min_bright"] - orion_stars["max_bright"]
#columns = ["name", "const", "ra", "dec", "max_bright", "min_bright"]
#orion_wide = orion_stars.loc[orion_stars["brightness_difference"] >= 1, columns]
#observable = orion_wide[orion_wide["min_bright"] <= 10.0]

#Create a final table for output and print it
final = orion_stars

print("Interesting stars in Orion:")
for item in final.iterrows():
    index, row = item     # 'item' is a pair. Split it into components.
    print("star =", row[0], row[1])
    print("maximum brightness =", row[4])
    print("minimum brightness =", row[5])
    print("right ascencsion =", row[2])
    print("declension = ", row[3], "\n")

print("Number of elements in 'final' is "+str(final.size))
print("The number of rows in 'final' is "+str(final.shape[0]))
print("The number of cols in 'final' is "+str(final.shape[1]))
print("The columns are "+str(list(final.columns.values)))
print("\nGPS coordinates are: "+str(gpsLat)+", "+str(gpsLong))
print("\nThe date and time is: "+str(date))