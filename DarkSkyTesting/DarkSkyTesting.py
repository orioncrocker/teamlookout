import time as time
import requests as req
import json


gpsLocs = [
    (45.554468, -122.900896),  # 26W Rock Creek exit
    (45.541845, -122.867680),  # 26W Tanasbourne exit
    (45.532377, -122.842351)  # 26W Bethany exit
#    ()   # 26W exit
]

times = [
    time.strptime("2020-01-02 05:00:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 05:01:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 05:05:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 05:10:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 05:15:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 06:00:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 06:30:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 08:00:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 12:00:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 16:00:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 20:00:00", "%Y-%m-%d %H:%M:%S"),
    time.strptime("2020-01-02 23:59:00", "%Y-%m-%d %H:%M:%S")
]

apiKeyDaniel = "daac1138e07b116d9188af572823756d"

for iTime in range(len(times)):
    for iGps in range(len(gpsLocs)):
        reqString = "https://api.darksky.net/forecast/" + \
            apiKeyDaniel + "/" + \
            str(gpsLocs[iGps][0]) + "," + str(gpsLocs[iGps][1]) + \
            "," + str(int(time.mktime(times[iTime])))
        #
        res = req.get(reqString)
        #print(res.text)[0:300]
        item = json.loads(res.text)
        #
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['currently']['time'])) + ',' +
              str(item['latitude']) + ',' + str(item['longitude']) + ',' +
              str(item['currently']['precipType']) + ',' +
              str(item['currently']['precipProbability']) + ',' +
              str(item['currently']['temperature']) + ',')

# Handy code for converting times
# Displaying as string
# time.strftime("%Y-%m-%d %H:%M:%S", times[1])
# time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item['currently']['time']))
# Converting string into a epoch number for DarkSky request
# int(time.mktime(times[2]))
# Note the discrepancy between local and GMT??? Looks like none
# str(int(time.mktime(time.localtime())))
#     int(time.mktime(time.localtime()))
