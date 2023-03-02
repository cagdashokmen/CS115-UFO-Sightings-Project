# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 18:35:01 2020

@author: Çağdaş
"""

import numpy as np

output=""

def getfilerows(f):
    filerows = f.read().splitlines()
    return filerows[1:]

def getneededvalues(rows):
    result = []
    for row in rows:
        rowvalues = row.split(',')
        rowvalues.pop(8)
        rowvalues.pop(7)
        rowvalues.pop(6)
        rowvalues.pop(2)
        rowvalues[6] = float(rowvalues[6])
        rowvalues[5] = float(rowvalues[5])
        rowvalues[4] = float(rowvalues[4])
        yearandtotalminutes = getyearandtotalminutes(rowvalues[0])
        rowvalues[0] = yearandtotalminutes[1]
        rowvalues.insert(0,yearandtotalminutes[0])
        
        
        result.append(rowvalues)
    return result

def getyearandtotalminutes(time):
    splitted = time.split(' ')
    year = int(splitted[0].split('/')[-1])
    hoursminutes = splitted[1].split(':')
    hours = hoursminutes[0]
    minutes = hoursminutes[1]
    return (year, int(hours) * 60 + int(minutes))

def gettimefromminutes(minutes):
    return "{:02d}:{:02d}".format(int(minutes / 60), int(minutes % 60))

def getmostseenshapesbycountry(npa):
    countries = {}
    for data in npa[:,[3,4]]:
        country = data[0]
        shape = data[1]
        if country:
            if not country in countries:
                countries[country] = {}
            if not shape in countries[country]:
                countries[country][shape] = 0
            countries[country][shape] += 1
    return countries

def getmostseenshapeincountry(country):
    shapename = 0
    count = 0
    for shape in country:
        if country[shape] > count:
            shapename = shape
            count = country[shape]
    return (shapename, count)

def getmostseenyear(npa):
    years = npa[:,0]
    counts = {}
    for year in years:
        if not year in counts:
            counts[year]= 0
        counts[year] += 1
    mostseenyear = 0
    mostseencount = 0
    for year in counts:
        if counts[year] > mostseencount:
            mostseenyear = year
            mostseencount = counts[year]
    return (mostseenyear, mostseencount)

def getmostseencity(npa):
    cities = npa[:,2]
    counts = {}
    for city in cities:
        if not city in counts:
            counts[city]= 0
        counts[city] += 1
    mostseencity = 0
    mostseencount = 0
    for city in counts:
        if counts[city] > mostseencount:
            mostseencity = city
            mostseencount = counts[city]
    return (mostseencity, mostseencount)

def getmostseencitybyyear(npa, year):
    cities = npa[npa[:,0] == year][:,2]
    counts = {}
    for city in cities:
        if not city in counts:
            counts[city]= 0
        counts[city] += 1
    mostseencity = 0
    mostseencount = 0
    for city in counts:
        if counts[city] > mostseencount:
            mostseencity = city
            mostseencount = counts[city]
    return (mostseencity, mostseencount)

def getinfooflongestsight(npa):
    longest = npa[0]
    for sighting in npa:
        if sighting[5] > longest[5]:
            longest = sighting
    return ( "{} - {}".format(sighting[3],sighting[2]).upper(), sighting[0], gettimefromminutes(sighting[1]), int(sighting[5]), sighting[6], sighting[7])

def printandstoreoutput(text=""):
    global output
    print(text)
    output += "{}\n".format(text)

f = open('ufo-sightings.csv')
npa = np.array(getneededvalues(getfilerows(f)), dtype=object)
f.close()

printandstoreoutput("There are {} UFO sightings records in the dataset.".format(npa.shape[0]))
printandstoreoutput()

averagehour = gettimefromminutes(npa[:,1].mean())
printandstoreoutput("Average time UFO seen: {}".format(averagehour))
printandstoreoutput()

printandstoreoutput("Most seen shapes by countries:")
countries = getmostseenshapesbycountry(npa)
for country in countries:
    mostseenshape = getmostseenshapeincountry(countries[country])
    printandstoreoutput("{}: Shape '{}' with {} sightings.".format(country.upper(),mostseenshape[0],mostseenshape[1]))
printandstoreoutput()

mostseenyear = getmostseenyear(npa)
printandstoreoutput("The most UFO seen year is {} with {} sightings.".format(mostseenyear[0],mostseenyear[1]))
printandstoreoutput()

mostseencity = getmostseencity(npa)
printandstoreoutput("The most UFO seen city is {} with {} sightings.".format(mostseencity[0].upper(),mostseencity[1]))
printandstoreoutput()

selectedyear = 1966 # you can change this year to get the most UFO seen city in selectedyear
mostseencitybyyear = getmostseencitybyyear(npa, selectedyear)
printandstoreoutput("The most UFO seen city is {} with {} sightings in {}.".format(mostseencitybyyear[0].upper(), mostseencitybyyear[1], selectedyear))
printandstoreoutput()

infooflongestsight = getinfooflongestsight(npa)
printandstoreoutput("Informations of the UFO sighting with longest duration:")
printandstoreoutput("\tLocation: {}".format(infooflongestsight[0]))
printandstoreoutput("\tYear: {}".format(infooflongestsight[1]))
printandstoreoutput("\tTime of day: {}".format(infooflongestsight[2]))
printandstoreoutput("\tDuration: {} seconds".format(infooflongestsight[3]))
printandstoreoutput("\tCoordinates:")
printandstoreoutput("\t\tLatitude : {}".format(infooflongestsight[4]))
printandstoreoutput("\t\tLongitude: {}".format(infooflongestsight[5]))


fo = open("output.txt", "w")
fo.write(output)
fo.close()