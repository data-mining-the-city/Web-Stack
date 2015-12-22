#DMC TEAM KUAILE SERVER CODE
#Note: you must pre-process the Weibo dataset to add the CNY value to Users, to add lat and lng values to Checkins

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

#daymaker makes your day
def daymaker(time):
	temp = str(time)
	tempYear = str(temp[0:4])
	tempMonth = str(temp[5:7])
	tempDay = str(temp[8:10])
	dayscore = 0

	tempDate = datetime.date(int(tempYear), int(tempMonth), int(tempDay))

	if datetime.date(2014, 1, 15) <= tempDate <= datetime.date(2014,02, 12):
		dayscore = tempDate - datetime.date(2014, 1, 15)
	else:
		dayscore = 0

	return dayscore.days

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

		#FIRST QUERY TO DATABASE, FILTERING USERS AND LIMITING TO 10
        query = 'SELECT * FROM USER WHERE CNY = 7 limit 20'


	records = client.command(query)

	numListings = len(records)
	print 'received ' + str(numListings) + ' users'

	output = {"type":"FeatureCollection","features":[]}

	userDict = {}

	for user in records:
			userDict[user.uid] = {}

	for i, uid in enumerate(userDict.keys()):

			print 'looking at user ' + str(uid)
			q.put('processing ' + str(i) + ' out of ' + str(numListings) + ' users...')

			#SECOND QUERY TO DATABASE, GETTING CHECKINS FOR USER
			s = "SELECT expand(out_Checkin) FROM User WHERE uid = {}"

			checkins = client.command(s.format(uid))

			polylines = []

			numCheckins = len(checkins)
			cids = [checkin.cid for checkin in checkins]
			print 'user ' + str(uid) + ' has ' + str(numCheckins) + ' checkins'

			userDict[uid]['checkins'] = set(cids)

			#THIRD AND FINAL QUERY TO DATABASE, FILTER CHECKINS
			for cid in userDict[uid]['checkins']:

				t = "SELECT lat, lng, time, cat_1 FROM CHECKIN WHERE cid = {} AND time BETWEEN '2014-01-21 00:01:00' AND '2014-02-13 00:00:00'"
				#Note that query is not limited geographically: performance varied with number of users found.
				#AND lat BETWEEN {} AND {} AND lng BETWEEN {} AND {}"

				CNYcheckins = client.command(t.format(cid, lat1, lat2, lng1, lng2))
				testBool = len(CNYcheckins)

				print 'querying ' + str(cid) + ' for user ' + str(uid)

				if len(CNYcheckins)!=0:

					print 'great success!'

					for j, CNYcheckin in enumerate(CNYcheckins):

						q.put(str(j) + ' out of ' + str(numCheckins) + ' valid ...')

						feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
						feature ["user"] = uid
						feature ["properties"]["time"] = daymaker(CNYcheckin.time)
						feature ["properties"]["type"] = CNYcheckin.cat_1
						feature["geometry"]["coordinates"] = [CNYcheckin.lat, CNYcheckin.lng]
						print feature ["properties"]["time"]

						output["features"].append(feature)
						polylines.append({'coordinates'	: [CNYcheckin.lat, CNYcheckin.lng]})

			output["polylines"] = polylines

			q.put('idle')

	client.db_close()

	return json.dumps(output)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)
