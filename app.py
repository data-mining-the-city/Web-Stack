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

#def point_distance(x1, y1, x2, y2):
#	return ((x1-x2)**2.0 + (y1-y2)**2.0)**(0.5)

#def remap(value, min1, max1, min2, max2):
#	return float(min2) + (float(value) - float(min1)) * (float(max2) - float(min2)) / (float(max1) - float(min1))

#def normalizeArray(inputArray):
#	maxVal = 0
#	minVal = 100000000000

#	for j in range(len(inputArray)):
#		for i in range(len(inputArray[j])):
#			if inputArray[j][i] > maxVal:
#				maxVal = inputArray[j][i]
#			if inputArray[j][i] < minVal:
#				minVal = inputArray[j][i]

#	for j in range(len(inputArray)):
#		for i in range(len(inputArray[j])):
#			inputArray[j][i] = remap(inputArray[j][i], minVal, maxVal, 0, 1)

#	return inputArray

#def event_stream():
#    while True:
#        result = q.get()
#        yield 'data: %s\n\n' % str(result)

#@app.route('/eventSource/')
#def sse_source():
#    return Response(
#            event_stream(),
#            mimetype='text/event-stream')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getData/")
def getData():

	#q.put("starting data query...")

	#lat1 = str(request.args.get('lat1'))
	#lng1 = str(request.args.get('lng1'))
	#lat2 = str(request.args.get('lat2'))
	#lng2 = str(request.args.get('lng2'))

	#w = float(request.args.get('w'))
	#h = float(request.args.get('h'))
	#cell_size = float(request.args.get('cell_size'))

	#analysis = request.args.get('analysis')

	#CAPTURE ANY ADDITIONAL ARGUMENTS SENT FROM THE CLIENT HERE

	#print "received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"

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



        query = 'SELECT lat, lng, cat_2, title FROM Place WHERE cat_1 = "Outdoors" AND city = 0752'
	records = client.command(query)
	#USE INFORMATION RECEIVED FROM CLIENT TO CONTROL	#HOW MANY RECORDS ARE CONSIDERED IN THE ANALYSIS

	# random.shuffle(records)
	# records = records[:100]

	numListings = len(records)
	print 'received ' + str(numListings) + ' records'

	client.db_close()

 	#iterate through data to find minimum and maximum price
	#minPrice = 1000000000
	#maxPrice =

	#for record in records:
	#	price = record.price

	#	if price > maxPrice:
	#		maxPrice = price
	#	if price < minPrice:
	#		minPrice = price

	#print minPrice
	#print maxPrice

	output = {"type":"FeatureCollection","features":[]}

        for record in records:
            feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
            feature["properties"]["category"]= record.cat_2
            feature["properties"]["title"]= record.title
            feature["geometry"]["coordinates"]=[record.lat, record.lng]

            output["features"].append(feature)

	#if analysis == "false":
	#	q.put('idle')
	#	return json.dumps(output)

	#q.put('starting analysis...')

	#output["analysis"] = []

	#numW = int(math.floor(w/cell_size))
	#numH = int(math.floor(h/cell_size))

	#grid = []

	#for j in range(numH):
	#	grid.append([])
	#	for i in range(numW):
	#		grid[j].append(0)

	#USE CONDITIONAL ALONG WITH UI INFORMATION RECEIVED FROM THE CLIENT TO SWITCH
	#BETWEEN HEAT MAP AND INTERPOLATION ANALYSIS

	## HEAT MAP IMPLEMENTATION
	# for record in records:

	# 	pos_x = int(remap(record.longitude, lng1, lng2, 0, numW))
	# 	pos_y = int(remap(record.latitude, lat1, lat2, numH, 0))

	#USE INFORMATION RECEIVED FROM CLIENT TO CONTROL SPREAD OF HEAT MAP
	# 	spread = 12

	# 	for j in range(max(0, (pos_y-spread)), min(numH, (pos_y+spread))):
	# 		for i in range(max(0, (pos_x-spread)), min(numW, (pos_x+spread))):
	# 			grid[j][i] += 2 * math.exp((-point_distance(i,j,pos_x,pos_y)**2)/(2*(spread/2)**2))


	## MACHINE LEARNING IMPLEMENTATION

	#featureData = []
	#targetData = []

	#for record in records:
	#	featureData.append([record.latitude, record.longitude])
	#	targetData.append(record.price)

	#X = np.asarray(featureData, dtype='float')
	#y = np.asarray(targetData, dtype='float')

	#breakpoint = int(numListings * .7)

	#print "length of dataset: " + str(numListings)
	#print "length of training set: " + str(breakpoint)
	#print "length of validation set: " + str(numListings-breakpoint)

	# create training and validation set
	#X_train = X[:breakpoint]
	#X_val = X[breakpoint:]

	#y_train = y[:breakpoint]
	#y_val = y[breakpoint:]

	#mean 0, variance 1
	#scaler = preprocessing.StandardScaler().fit(X_train)
	#X_train_scaled = scaler.transform(X_train)

	#mse_min = 10000000000000000000000

	#for C in [.01, 1, 100, 10000, 1000000]:

	#	for e in [.01, 1, 100, 10000, 1000000]:

	#			for g in [.01, 1, 100, 10000, 1000000]:

	#				q.put("training model: C[" + str(C) + "], e[" + str(e) + "], g[" + str(g) + "]")

	#				model = svm.SVR(C=C, epsilon=e, gamma=g, kernel='rbf', cache_size=2000)
	#				model.fit(X_train_scaled, y_train)

	#				y_val_p = [model.predict(i) for i in X_val]

	#				mse = 0
	#				for i in range(len(y_val_p)):
	#					mse += (y_val_p[i] - y_val[i]) ** 2
	#				mse /= len(y_val_p)

	#				if mse < mse_min:
	#					mse_min = mse
	#					model_best = model
	#					C_best = C
	#					e_best = e
	#					g_best = g

	#q.put("best model: C[" + str(C_best) + "], e[" + str(e_best) + "], g[" + str(g_best) + "]")

	#for j in range(numH):
	#	for i in range(numW):
	#		lat = remap(j, numH, 0, lat1, lat2)
	#		lng = remap(i, 0, numW, lng1, lng2)

	#		testData = [[lat, lng]]
	#		X_test = np.asarray(testData, dtype='float')
	#		X_test_scaled = scaler.transform(X_test)
	#		grid[j][i] = model_best.predict(X_test_scaled)



	#grid = normalizeArray(grid)

	#offsetLeft = (w - numW * cell_size) / 2.0
	#offsetTop = (h - numH * cell_size) / 2.0

	#for j in range(numH):
	#	for i in range(numW):
	#		newItem = {}

	#		newItem['x'] = offsetLeft + i*cell_size
	#		newItem['y'] = offsetTop + j*cell_size
	#		newItem['width'] = cell_size-1
	#		newItem['height'] = cell_size-1
	#		newItem['value'] = grid[j][i]

	#		output["analysis"].append(newItem)

	# q.put('idle')

	return json.dumps(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
