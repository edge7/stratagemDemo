
#### Import ####
import sys
import os
import re 
####        ####


#### Utility Functions ####

def fileExistsAndNotEmpty( filePath ) :
    existsAndNotEmpty = False
    try:
        if os.stat(filePath).st_size > 0:
           existsAndNotEmpty = True
        else:
           print "empty file"
    except OSError:
           print "No file"

    return existsAndNotEmpty

####                   ####

usage = "Run the script: ./fromTickToTimeFrame.py tickDataFile timeFrame_minutes"

if len(sys.argv) != 3 :
    print(usage)
    sys.exit(0)

if len(sys.argv) > 1:
    tickDataName = sys.argv[1]
    timeFrame = sys.argv[2]

#Checking if timeFrame is an integer between 1 and 60
try:
   timeFrame = int(timeFrame)
except ValueError:
   print(" timeFrame must be between 1 and 60 integer value")
   sys.exit(0)

# Checking if file exists and it is not empty 
if fileExistsAndNotEmpty( tickDataName) == False :
    print "There was an error opening" + tickDataName
    sys.exit(0)

# Opening file in read mode
tickDataFile = open(tickDataName, 'r')

# Creating a new file to write the processing output 
candleStickPath = tickDataName + "_" + "candleStick_" + str(timeFrame)
candleStickFile = open( candleStickPath , "w")

openT = 0.0
high = sys.float_info.min
low = sys.float_info.max
close = 0.0
counter = 0

#Looping on inputFile to process that 
for line in tickDataFile:

    #Each line is something like: 'EUR/USD,20150101 21:43:43,1.21'

    # Getting time, i.e.: 20150101 21:43:43
    time = line.split(",")[1]

    # Getting hour, i.e.: time
    # Getting minute as a integer, i.e.: 43 
    minutes = int( time.split(":")[1] ) 

    # Getting current Bid Price
    current_price = float(line.split(",")[2])

    #If needed, update init_time and open Price of the current candle 
    if counter == 0 :
       init_time = minutes 
       openT = current_price

    counter += 1 

    #If needed, update max ..
    if current_price > high :
       high = current_price
    # .. and low 
    if current_price < low :
       low = current_price

    # Checking if candle can be built  
    if abs( minutes - init_time) >= timeFrame :
       close = current_price
       counter = 0
       hour = int( re.search("\ \d\d", time).group(0) )
       candleStickFile.write(str(hour) + "," + str(minutes) + "," + str(openT) + "," + str(high) + "," + str(low) + "," + str(close) + "\n")
       high = sys.float_info.min
       low = sys.float_info.max
## End of the LOOP ###


### Closing file descriptor ###
tickDataFile.close()
candleStickFile.close()


