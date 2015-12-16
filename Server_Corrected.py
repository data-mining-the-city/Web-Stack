#######################################################################
#####################INDEX TIME in OrientDB FIRST!!!###################
#######################################################################

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


import time

import numpy as np
import matplotlib.pyplot as plt


app = Flask(__name__)

q = Queue()

##############heat map display########
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

	q.put("starting data query...") ##### status display#####

	startstr = str(request.args.get('starttime'))
	endstr = str(request.args.get('endtime'))

	################################map bound & window bound##############################
	lat1 = str(request.args.get('lat1'))
	lng1 = str(request.args.get('lng1'))
	lat2 = str(request.args.get('lat2'))
	lng2 = str(request.args.get('lng2'))

	w = float(request.args.get('w'))
	h = float(request.args.get('h'))

	#############################cellsize###############################
	# cell_size = float(request.args.get('cell_size'))

	############################analysis trigger########################
	# analysis = request.args.get('analysis')

	print "received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"

	
	client = pyorient.OrientDB("localhost", 2424)
	session_id = client.connect("root", "admin")
	db_name = "weibo"
	db_username = "admin"
	db_password = "admin"

	if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
		client.db_open( db_name, db_username, db_password )
		print db_name + " opened successfully"
	else:
		print "database [" + db_name + "] does not exist! session ending..."
		sys.exit()

#########################################################################
#####################CATEGORY NAME CHECK PLEASE!!!!!#####################
	query = 'SELECT  FROM Checkin WHERE time Between "{}" AND "{}" AND lat BETWEEN {} AND {} AND lng BETWEEN {} AND {} limit 200'
	results = client.command(query.format(startstr,endstr,lat1,lat2,lng1,lng2))
	

	output = {"type":"FeatureCollection","features":[]}

	for record in results:
	
		feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
		feature["id"] = record._rid
		feature["geometry"]["coordinates"] = [record.lat, record.lng]
		feature["time"] = str(record.time)
		feature["cat_1"] = record.cat_1
		feature["cat_2"] = record.cat_2
		feature["TOD"] = record.TOD
		feature["DOW"] = record.DOW
		output["features"].append(feature)

	client.db_close()
	# if analysis == "false":
	# 	q.put('idle')
	# 	return json.dumps(output)

	# q.put('starting analysis...') ##### status display#####

	# output["analysis"] = []

	# numW = int(math.floor(w/cell_size))
	# numH = int(math.floor(h/cell_size))

	# grid = []

	# for j in range(numH):
	# 	grid.append([])
	# 	for i in range(numW):
	# 		grid[j].append(0)

	# #HEAT MAP IMPLEMENTATION
	# for record in records:

	#  	pos_x = int(remap(record.longitude, lng1, lng2, 0, numW))
	#  	pos_y = int(remap(record.latitude, lat1, lat2, numH, 0))

	#  	spread = 12

	#  	for j in range(max(0, (pos_y-spread)), min(numH, (pos_y+spread))):
	#  		for i in range(max(0, (pos_x-spread)), min(numW, (pos_x+spread))):
	#  			grid[j][i] += 2 * math.exp((-point_distance(i,j,pos_x,pos_y)**2)/(2*(spread/2)**2))

		## ML IMPLEMENTATION
	# grid = normalizeArray(grid)

	# offsetLeft = (w - numW * cell_size) / 2.0
	# offsetTop = (h - numH * cell_size) / 2.0


	# for j in range(numH):
	#     for i in range(numW):
	#         newItem = {}

	# 		newItem['x'] = offsetLeft + i*cell_size
	# 		newItem['y'] = offsetTop + j*cell_size
	#         newItem['width'] = cell_size-1
	#         newItem['height'] = cell_size-1
	#         newItem['value'] = grid[j][i]

	#         output["analysis"].append(newItem)
	q.put('idle')
	return json.dumps(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
