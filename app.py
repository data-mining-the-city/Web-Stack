from flask import Flask
from flask import render_template
from flask import request
from flask import Response

import json
import time
import sys
import random
import math
import datetime

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

	print request.args.get('w')

	w = float(request.args.get('w'))
	h = float(request.args.get('h'))
	cell_size = float(request.args.get('cell_size'))

	analysis = request.args.get('analysis')

	# Setting up global variables that would be used in the query
	# Getting "day of week" and "time of day" information selected from the dropdown menu on the client side
	dropdownDay = request.args.get('dayOfWeek')
	dropdownTime = request.args.get('timeOfDay')

	print "received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"
	
	client = pyorient.OrientDB("localhost", 2424)
	session_id = client.connect("root", "michael2464")
	db_name = "weibo"
	db_username = "admin"
	db_password = "admin"

	if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
		client.db_open( db_name, db_username, db_password )
		print db_name + " opened successfully"
	else:
		print "database [" + db_name + "] does not exist! session ending..."
		sys.exit()

	# Set the checkin category to "Food"
	# Query data on the selected "day of week" and "time of day" from the weibo database
	query = 'SELECT FROM Checkin WHERE lat BETWEEN {} AND {} AND lng BETWEEN {} AND {} AND cat_1 = "Food" AND DOW =' + str(dropdownDay) + ' AND TOD = ' + str(dropdownTime)

	records = client.command(query.format(lat1, lat2, lng1, lng2))

	numListings = len(records)
	
	#print 'received ' + str(numListings) + ' records'
	q.put('received ' + str(numListings) + ' records')
        
	
	client.db_close()
        
	output = {"type":"FeatureCollection","features":[],"time":[]}

	for record in records:

		feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
		feature["id"] = record._rid
		feature["properties"]["time"] = str(record.time)
		feature["geometry"]["coordinates"] = [record.lat, record.lng]

		dateTimeList = str(record.time).split()
		date = dateTimeList[0]
		dateList = date.split('-')
		month = str(dateList[1])
		day = int(dateList[2])

		#calculating which day in the week
		seven = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		feature["properties"]["day"] = seven[record.time.weekday()]

		output["features"].append(feature)


	if analysis == "false":
		#q.put('idle')
		return json.dumps(output)

	#Calculating the heat map
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

		pos_x = int(remap(record.lng, lng1, lng2, 0, numW))
		pos_y = int(remap(record.lat, lat1, lat2, numH, 0))

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