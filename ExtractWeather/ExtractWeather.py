#!/usr/local/bin/python3

# This script generates a CSV file containing weather info for the time and
# region in question

import csv
import requests
import json
import time


# Read API key for DarkSky weather requests. The file should contain an API key string
# on the first line.
with open('./DarkSkyApiKey.txt', 'r') as f:
    darkSkyKey = f.readline()
    f.close()

# Start writing CSV file with weather info
with open('./weather.csv', 'w') as outFile:
    outWriter = csv.writer(outFile)
    # write column headers
    outWriter.writerow(['id', 'lat', 'long', 'datetime',   # keys
                        'summary',
                        'precipIntensity',
        #-- TODO precipProbability is probably just for _forecasts_... Is it in any of our 'current' data?
        #-- precipProbability FLOAT()	-- The lowest number I've seen is 0.01
                        'temperature',
                        'apparentTemperature',
                        'humidity',
                        'windSpeed',
                        'windGust',
                        'cloudCover',
                        'uvIndex',
                        'visibility'])

    # defaultLocation is in the middle of the area of interest and probably representative of
    # the weather at every detector id, since the locations are only maximum 5 miles apart.
    defaultLocation = ('45.528047', '-122.686994')
    # gpsLocs hold all the locations we want to look at. For now, it's just defaultLocation
    # but it could be fine-grained like one per detector
    gpsLocs = [defaultLocation]

    def getDaysInMonth(month, year):
        if month == 4 or month == 6 or month == 9 or month == 11:
            return 30
        if month == 2:
            if year % 4 == 0:
                return 29
            else:
                return 28
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            return 31


    primaryKey = 0
    for year in [2016]:     # range(2016, 2017) is not included in traffic at the moment
        for month in range(1, 3):   # 13):      i.e Jan-Dec inclusie
            for day in range(1, 3): #getDaysInMonth(month, year) + 1):
                for hour in range(0, 2):    # 23):
                    primaryKey += 1
                    baseDateTime = str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + \
                        " " + str(hour).zfill(2) + ":00:00"
                    epochTimeStr = str(int(time.mktime(time.strptime(baseDateTime, "%Y-%m-%d %H:%M:%S"))))
                    for gpsLoc in gpsLocs:
                        reqString = 'https://api.darksky.net/forecast/' + \
                            darkSkyKey + '/' + \
                            str(gpsLoc[0]) + ',' + str(gpsLoc[1]) + \
                            ',' + epochTimeStr
                        res = requests.get(reqString)
                        item = json.loads(res.text)
                        curWeather = item['currently']
                        outWriter.writerow([
                            str(primaryKey),
                            gpsLoc[0],
                            gpsLoc[1],
                            baseDateTime,
                            curWeather['summary'],
                            curWeather['precipIntensity'],
                            curWeather['temperature'],
                            curWeather['apparentTemperature'],
                            curWeather['humidity'],
                            curWeather['windSpeed'],
                            curWeather['windGust'],
                            curWeather['cloudCover'],
                            curWeather['uvIndex'],
                            curWeather['visibility']
                        ])


''' Database-related code
This is disabled and maybe not needed. It existed so that this script could
request weather information for ODOT crashes and other time that don't exactly
match the generic hourly time blocks we currently get from Dark Sky

#import psycopg2     # to access PostgreSQL db

# Read username and password file to connect to our SQL DB
with open('DbLogin.txt', 'r') as f:
    user = f.readline()
    password = f.readline()
    f.close()
    
try:
    conn = psycopg2.connect(host='learn-pgsql.rc.pdx.edu', database='cs510lookout', user=user, password=password)
except Exception as e:
    print('[!]', e)
else:
    cursor = conn.cursor()
    conn.execute("""
        SELECT distinct (detectorid, starttime) 
                FROM traffic
                ORDER BY detectorid, starttime;
        """)

    rowCount = 0
    for row in cursor:
        rowCount += 1
        # Convert db starttime into the epoch format that DarkSky uses
        #dsStartTime =

    cursor.close()
finally:
    conn.close()
'''
