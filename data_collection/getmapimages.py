import csv
import urllib
import os
from os.path import isfile, join
import time
import random

UScitylist = {}

with open('GL2_city_loc.csv','rb') as csvfile:
    reader = csv.reader(csvfile,delimiter='\t')
    for row in reader:
        if (row[3]=="US"):
            if row[6] in UScitylist.keys():
                UScitylist[row[6]].append(row[7])
            else:
                UScitylist[row[6]] = []
                UScitylist[row[6]].append(row[7])

#print UScitylist['Illinois']

roadmapurl = "https://maps.googleapis.com/maps/api/staticmap?zoom=18&size=800x800&maptype=roadmap"
satelliteurl = "https://maps.googleapis.com/maps/api/staticmap?zoom=18&size=800x800&maptype=satellite"

for city in UScitylist['Texas']:
    urllib.urlretrieve(roadmapurl+"&center="+city, "mapdata/"+city+"_Texas_roadmap.png")
    urllib.urlretrieve(satelliteurl+"&center="+city, "mapdata/"+city+"_Texas_satellite.png")
    time.sleep(3 + random.random())
    
onlyfiles = [ f for f in os.listdir("mapdata/") if isfile(join("mapdata/",f)) ]

#for i in onlyfiles:
#    city = i.split('_')
#    time.sleep(2)
    #print satelliteurl+"&center="+city[0].lower()
#    urllib.urlretrieve(satelliteurl+"&center="+city[0].lower(), "mapdata/"+city[0]+"_Illinois_satellite.png")
