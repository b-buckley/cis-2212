from sqlalchemy import create_engine
import pyodbc
import pandas as pd

constName = "Cas"

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
orion_stars["brightness_difference"] = orion_stars["min_bright"] - orion_stars["max_bright"]
columns = ["name", "const", "ra", "dec", "max_bright", "min_bright"]
orion_wide = orion_stars.loc[orion_stars["brightness_difference"] >= 1, columns]
observable = orion_wide[orion_wide["min_bright"] <= 10.0]

print("Interesting stars in Orion:")
for item in observable.iterrows():
    index, row = item     # 'item' is a pair. Split it into components.
    print("star =", row[0], row[1])
    print("maximum brightness =", row[4])
    print("minimum brightness =", row[5])
    print("right ascencsion =", row[2])
    print("declension = ", row[3], "\n")