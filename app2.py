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

        query = 'SELECT * FROM USER WHERE CNY = 7 limit 2'
        #lat BETWEEN {} AND {} AND lng BETWEEN {} AND {} AND time BETWEEN "2014-01-21 00:01:00" and "2014-02-13 00:00:00"

	records = client.command(query)

	numListings = len(records)
	print 'received ' + str(numListings) + ' users'

	userDict = {}
	scoreDict = {}

	for user in records:
		userDict[user._rid] = {}
		scoreDict[user._rid] = 0

	for i, rid in enumerate(userDict.keys()):

		print str(rid)
		q.put('processing ' + str(i) + ' out of ' + str(numListings) + ' users...')

		s = "SELECT expand(out_Checkin) FROM User WHERE uid = {}"

		checkins = client.command(s.format(rid))
		cids = [checkin.cid for checkin in checkins]

		userDict[rid]['checkins'] = set(cids)
		print str(userDict[rid]['checkins'])
		#for checkin in checkins:
			#print checkin.cid


	#Third and final query to databse, filtering previous checkins by time and location to get the ones we want.
		for cid in userDict[rid]['checkins']:

			t = "SELECT lat, lng FROM CHECKIN WHERE cid = {} AND time BETWEEN '2014-01-21 00:01:00' AND '2014-02-13 00:00:00' AND lat BETWEEN {} AND {} AND lng BETWEEN {} AND {}"

			CNYcheckins = client.command(t.format(cid, lat1, lat2, lng1, lng2))
			CNYcids = [CNYcheckin.cid for CNYcheckin in CNYcheckins]

			userDict[rid]['CNYcheckins'] = set(CNYcids)

	q.put ('Matching records..')

	lines = []

	#for user1 in userDict.keys():
	#	checkin1 = userDict[user1]['checkins']
	#	userDict.pop(user1)
	#		if len(users1 & userDict[user2]['users']) > 1:
	#			scoreDict[user1] += 1
	#			scoreDict[user2] += 1
	#			lines.append({'from': user1, 'to': user2, 'coordinates': [lat1, lng1, userDict[user2]['lat'], userDict[user2]['lng']]})

	client.db_close()


	#output = {"type":"FeatureCollection","features":[]}

	for CNYcheckin in CNYcheckins:
		feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
		feature["id"] = CHYcheckin._cid
		feature["geometry"]["coordinates"] = [CNYcheckin.lat, CNYcheckin.lng]

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

        #client.db_close()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
