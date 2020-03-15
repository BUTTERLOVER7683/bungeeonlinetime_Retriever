import pymysql
from mcuuid.api import GetPlayerData
import xlsxwriter
import os

# Deletes old Excel workbook if present
if os.path.exists("SQLTimePlayed.xlsx"):
    # Checks if the Excel workbook is open
    try:
        os.remove("SQLTimePlayed.xlsx")
        print("Prior Workbook Removed")
    except PermissionError:
        # **Inputs used throughout for those running through a shell**
        input("Prior Workbook In Use! Please close before continuing!")
        quit()
else:
    print("No Prior Workbook Found")

# Initializing Excel Sheet
wb = xlsxwriter.Workbook('SQLTimePlayed.xlsx')
sheet = wb.add_worksheet('time')
style0 = wb.add_format({'bold': True, 'bottom': True})
style1 = wb.add_format({'bold': True, 'font_color': 'red'})
sheet.write(0, 0, "Raw UUID", style0)
sheet.write(0, 1, "Player Name", style0)
sheet.write(0, 2, "Hours", style0)

# Ask for login information:
host = input("Host: ")
user = input("User: ")
password = input("Password: ")
database = input("Database: ")

# Database Login
db = ""
try:
    db = pymysql.connect(host, user, password, database)
except pymysql.err.OperationalError:
    input("Error: Host/User/Password Invalid")
    quit()
except pymysql.err.InternalError:
    input("Error: Bad Database Name")
    quit()

# Prepare Cursor
cursor = db.cursor()
# Ask for table name where times are stored
tablename = input("Table Name: ")
# Specify the query command
# Asks how many minimum hours a player needs to be included.
minhours = input("Minimum Hours Needed: ")
minhours = int(minhours) * 60
cmd1 = "SELECT * FROM %s WHERE onlinetime > %d" % (tablename, minhours)
# Obtain the data
try:
    # Executes query above (cmd1)
    cursor.execute(cmd1)
except pymysql.err.ProgrammingError:
    # Kill everything if command cannot execute
    input("Bad Query Syntax -or- Bad Table Name")
    exit()

# Fetches all data associated with query
tabledata = cursor.fetchall()

# Will go to second row when for loop starts
row = 0

# ***Display to console and writing to Excel sheet***
for entry in tabledata:
    # THIS IF CHECK CAN BE DELETED - HANDLED EARLIER
    # MCUUID does not accept full UUID, so it must be trimmed with replace function
    trimuuid = entry[0].replace("-", "")
    try:
        player = GetPlayerData(trimuuid)
    except:
        print("MCUUID ERROR AT - " + trimuuid)
        continue
    # Restart each for loop to first column and next row
    column = 0
    row += 1
    # Translates minutes from DB into hours (and rounds to two decimal points)
    tiH = round((int(entry[1] / 60)), 2)
    if player.valid is True:
        print("%s | %s | %d" % (player.uuid, player.username, tiH))
        sheet.write(row, column, player.uuid)
        sheet.write(row, column + 1, player.username)
        sheet.write(row, column + 2, tiH)
    elif player.valid is False:
        print("%s | INVALID UUID | %d" % (player.uuid, tiH))
        sheet.write(row, column, trimuuid)
        sheet.write(row, column + 1, "INVALID UUID", style1)
        sheet.write(row, column + 2, tiH)
    else:
        print("%s | VERY BADNESS | %d" % (player.uuid, tiH))
        sheet.write(row, column, trimuuid)
        sheet.write(row, column + 1, "VERY BAD", style1)
        sheet.write(row, column + 2, tiH)

# Close and save the Excel workbook
wb.close()
# Disconnect
db.close()
print("Data write completed and database disconnected!")
input("Press Enter To Continue")
