[![License](https://img.shields.io/badge/License-MIT-red.svg)](https://shields.io/)
# General Information

* This script is to be used in conjuction with the Bungeeonlinetime plugin (https://www.spigotmc.org/resources/bungeeonlinetime.795/).
* You MUST have your data stored in an SQL database. This will not work with a local flatfile.
* SSH Tunneling will (most likely) not work. - Untested, but likely
* Uses the **pymysql**, **mcuuid**, **xlsxwriter**, and **os** packages.
  * Might want to have these installed for it to work properly.

This script can be run from the Python shell effecively, with some tidbits of code accomodating for it. Of course, it can be run through programs like PyCharm.

This script will ask for login credentials for your SQL database and obtain the data within the 'bungeeonlinetime' table. It will
then translate the UUID's into Usernames, change the minutes in the database to hours, and output it all into an Excel workbook (which will be generated in the directory the 'main.py' script is in) named 'SQLTimePlayed.xlsx'.

This script has been writtin to give you as much information as possible about bugs that might pop up, but if you have any questions/issues, please make a report.

Feel free to make a pull request will any perceived improvements.

### License
This code is protected under the MIT License. Feel free to use it as you see fit, but I encourage you to make any derivations open-sourced out of the kindness of your heart.
