from flask import Flask
from flask import render_template
from flask import request
from flask import Response

import json
import time
import sys
import random
import math

import pyorient

from Queue import Queue

from sklearn import preprocessing
from sklearn import svm

import numpy as np

app = Flask(__name__)

q = Queue()

def point_distance(x1, y1, x2, y2):
	return ((x1-x2)**2.0 + (y1-y2)**2.0)**(0.5)

def remap(value, min1, max1, min2, max2):
	return float(min2) + (float(value) - float(min1)) * (float(max2) - float(min2)) / (float(max1) - float(min1))

def normalizeArray(inputArray):
	maxVal = 0
	minVal = 100000000000

	for j in range(len(inputArray)):
		for i in range(len(inputArray[j])):
			if inputArray[j][i] > maxVal:
				maxVal = inputArray[j][i]
			if inputArray[j][i] < minVal:
				minVal = inputArray[j][i]

	for j in range(len(inputArray)):
		for i in range(len(inputArray[j])):
			inputArray[j][i] = remap(inputArray[j][i], minVal, maxVal, 0, 1)

	return inputArray

def event_stream():
    while True:
        result = q.get()
        yield 'data: %s\n\n' % str(result)

@app.route('/eventSource/')
def sse_source():
    return Response(
            event_stream(),
            mimetype='text/event-stream')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getData/")
def getData():

	q.put("starting data query...")

	lat1 = str(request.args.get('lat1'))
	lng1 = str(request.args.get('lng1'))
	lat2 = str(request.args.get('lat2'))
	lng2 = str(request.args.get('lng2'))

	print "received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"

	#w = float(request.args.get('w'))
	#h = float(request.args.get('h'))
	#cell_size = float(request.args.get('cell_size'))

	#analysis = request.args.get('analysis')

	#CAPTURE ANY ADDITIONAL ARGUMENTS SENT FROM THE CLIENT HERE

	print "received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"

	client = pyorient.OrientDB("localhost", 2424)
	session_id = client.connect("root", "password")
	db_name = "weibo"
	db_username = "admin"
	db_password = "admin"

        if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
		client.db_open( db_name, db_username, db_password )
		print db_name + " opened successfully"
	else:
		print "database [" + db_name + "] does not exist! session ending..."
		sys.exit()

        query = 'SELECT * FROM USER WHERE CNY = 7 limit 1'
        #lat BETWEEN {} AND {} AND lng BETWEEN {} AND {} AND time BETWEEN "2014-01-21 00:01:00" and "2014-02-13 00:00:00"

	records = client.command(query.format())

	numListings = len(records)
	print 'received ' + str(numListings) + ' users'
	
	userDict = {}
	#scoreDict = {}

	for record in records:
		userDict[record._rid] = record.uid
		#scoreDict[place._rid] = 0    

	for i, rid in enumerate(userDict.keys()):

		q.put('processing ' + str(i) + ' out of ' + str(numListings) + ' users...')

		s = "SELECT expand(out_Checkin) FROM {} WHERE @class = 'User'"

		checkins = client.command(s.format(rid))
		for checkin in checkins:

  		#userDict[rid]["checkins"] = cids
		  print checkin.cid

	q.put('matching records...')

	#lines = []

	#for place1 in placesDict.keys():
	#	users1 = placesDict[place1]['users']
	#	lat1 = placesDict[place1]['lat']
	#	lng1 = placesDict[place1]['lng']
	#	placesDict.pop(place1)
	#	for place2 in placesDict.keys():
	#		if len(users1 & placesDict[place2]['users']) > 1:
	#			scoreDict[place1] += 1
	#			scoreDict[place2] += 1
	#			lines.append({'from': place1, 'to': place2, 'coordinates': [lat1, lng1, placesDict[place2]['lat'], placesDict[place2]['lng']]})

	client.db_close()


	#output = {"type":"FeatureCollection","features":[]}

	#for record in records:
	#	if scoreDict[record._rid] < 1:
	#		continue
	#	feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
	#	feature["id"] = record._rid
	#	feature["properties"]["name"] = record.title
	#	feature["properties"]["cat"] = record.cat_1
	#	feature["properties"]["score"] = scoreDict[record._rid]
	#	feature["geometry"]["coordinates"] = [record.lat, record.lng]

	#	output["features"].append(feature)


	#output["lines"] = lines
	
	#for record1 in records1:
	#    query2 = 'SELECT expand(out_Checkin) FROM USER WHERE uid = {}'
	 #    records2 = client.command(query2.format(record1))
	     
	 #    output2 = {"type":"FeatureCollection","features":[]}
	  #   for record2 in records2:
	   #    feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}   
	    #   feature["properties"]["checkin"]= str(record2.cid)
	     #  print  feature["properties"]["checkin"]
	       
	      # output2["features"].append(feature)

        #output = {"type":"FeatureCollection","features":[]}
        #add three sets of coordinates, times and checkins {UserID:{Check-In Time1: Check-In Location1}{Check-In Time2: Check-In Location2}{Check-In Time3: Check-In Location3}}
        #for record in records:
        #    feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
        #    feature["geometry"]["coordinates"]=[record.lat, record.lng]
        #    feature["properties"]["user"]= str(record.out)
	#    feature["properties"]["time"]= str(record.time)
        #    print feature["properties"]["user"]

        #    output["features"].append(feature)

	#return json.dumps(output)

        client.db_close()
        
@app.route("/getData2/")
def getData2():

	q.put("starting data query...")

	lat1 = str(request.args.get('lat1'))
	lng1 = str(request.args.get('lng1'))
	lat2 = str(request.args.get('lat2'))
	lng2 = str(request.args.get('lng2'))

	w = float(request.args.get('w'))
	h = float(request.args.get('h'))
	cell_size = float(request.args.get('cell_size'))

	analysis = request.args.get('analysis')

	print "also received coordinates for heat map: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"

	client = pyorient.OrientDB("localhost", 2424)
	session_id2 = client.connect("root", "password")
	db_name2 = "soufun"
	db_username2 = "admin"
	db_password2 = "admin"

	if client.db_exists( db_name2, pyorient.STORAGE_TYPE_MEMORY ):
		client.db_open( db_name2, db_username2, db_password2 )
		print db_name2 + " opened successfully"
	else:
		print "database [" + db_name2 + "] does not exist! session ending..."
		sys.exit()

	query = 'SELECT FROM Listing WHERE latitude BETWEEN {} AND {} AND longitude BETWEEN {} AND {}'

	records = client.command(query.format(lat1, lat2, lng1, lng2))

	random.shuffle(records)
	records = records[:100]

	numListings = len(records)
	print 'received ' + str(numListings) + ' records'

	client.db_close()

        minPrice = 1000000000
        maxPrice = 0

        for record in records:
            price = record.price

            if price > maxPrice:
                maxPrice = price
            if price < minPrice:
                minPrice = price

        print minPrice
        print maxPrice

	output = {"type":"FeatureCollection","features":[]}

	for record in records:
		feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
		feature["id"] = record._rid
		feature["properties"]["name"] = record.title
		feature["properties"]["price"] = record.price
		feature["geometry"]["coordinates"] = [record.latitude, record.longitude]

		output["features"].append(feature)

	if analysis == "false":
		q.put('idle')
		return json.dumps(output)

	q.put('starting analysis...')

	output["analysis"] = []

	numW = int(math.floor(w/cell_size))
	numH = int(math.floor(h/cell_size))

	grid = []

	for j in range(numH):
		grid.append([])
		for i in range(numW):
			grid[j].append(0)

	for record in records:

		pos_x = int(remap(record.longitude, lng1, lng2, 0, numW))
		pos_y = int(remap(record.latitude, lat1, lat2, numH, 0))

		#TRY TESTING DIFFERENT VALUES FOR THE SPREAD FACTOR TO SEE HOW THE HEAT MAP VISUALIZATION CHANGES
		spread = 12

		for j in range(max(0, (pos_y-spread)), min(numH, (pos_y+spread))):
			for i in range(max(0, (pos_x-spread)), min(numW, (pos_x+spread))):
				grid[j][i] += 2 * math.exp((-point_distance(i,j,pos_x,pos_y)**2)/(2*(spread/2)**2))

	grid = normalizeArray(grid)

	offsetLeft = (w - numW * cell_size) / 2.0
	offsetTop = (h - numH * cell_size) / 2.0

	for j in range(numH):
		for i in range(numW):
			newItem = {}

			newItem['x'] = offsetLeft + i*cell_size
			newItem['y'] = offsetTop + j*cell_size
			newItem['width'] = cell_size-1
			newItem['height'] = cell_size-1
			newItem['value'] = grid[j][i]

			output["analysis"].append(newItem)

	q.put('idle')

	return json.dumps(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
