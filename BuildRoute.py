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

import numpy as np

app = Flask(__name__)

#q = Queue()

#def remap(value, min1, max1, min2, max2):
	#return float(min2) + (float(value) - float(min1)) * (float(max2) - float(min2)) / (float(max1) - float(min1))

#def event_stream():
    #while True:
        #result = q.get()
        #yield 'data: %s\n\n' % str(result)

#@app.route('/eventSource/')
#def sse_source():
    #return Response(
            #event_stream(),
            #mimetype='text/event-stream')

#@app.route("/")
#def index():
    #return render_template("index.html")

@app.route("/getData/")
def getData():

	#q.put("starting data query...")

	#lat1 = str(request.args.get('lat1'))
	#lng1 = str(request.args.get('lng1'))
	#lat2 = str(request.args.get('lat2'))
	#lng2 = str(request.args.get('lng2'))

	#print "received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"
	
def filter_database():
	
    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect("root", "474F1CBE549F9E33FC8A0793C7819485072DAE07A4B704138010F28A28B69DF9")
    db_name = "weibo"
    db_username = "admin"
    db_password = "admin"

    if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
		client.db_open( db_name, db_username, db_password )
		print db_name + " opened successfully"
    else:
		print "database [" + db_name + "] does not exist! session ending..."
		sys.exit()

    query = 'SELECT FROM Checkin WHERE lat BETWEEN 22.929935 AND 22.961751 AND lng BETWEEN 113.639837 AND 113.693017 AND time BETWEEN "2014-09-03 03:00:00" and "2014-09-04 04:00:00"'
	   #houjie area selection
	
    records = client.command(query)
    #records = client.command(query.format(lat1,lat2, lng1, lng2))

    for record in records:
        
        print record
        person = client.command("SELECT expand(out) FROM {}".format(record._rid))
        print person
        places = client.command("SELECT * FROM (TRAVERSE out(Checkin) FROM (SELECT * FROM {})) WHERE @class = 'Place'".format(person[0]._rid))
        
        for place in places:
            print place._rid
	 

    numListings = len(records)
    print 'received ' + str(numListings) + ' records'

	#placesDict = {}
	#scoreDict = {}

	#for place in records:
		#placesDict[place._rid] = {'lat': place.lat, 'lng': place.lng}
		#scoreDict[place._rid] = 0

	#for i, rid in enumerate(placesDict.keys()):

		#q.put('processing ' + str(i) + ' out of ' + str(numListings) + ' places...')

		#s = "SELECT * FROM (TRAVERSE in(Checkin) FROM {}) WHERE @class = 'User'"

		#people = client.command(s.format(rid))
		#uids = [person.uid for person in people]

		#placesDict[rid]['users'] = set(uids)

	#q.put('matching records...')

	#lines = []

	#for place1 in placesDict.keys():
		#users1 = placesDict[place1]['users']
		#lat1 = placesDict[place1]['lat']
		#lng1 = placesDict[place1]['lng']
		#placesDict.pop(place1)
		#for place2 in placesDict.keys():
			#if len(users1 & placesDict[place2]['users']) > 1:
				#scoreDict[place1] += 1
				#scoreDict[place2] += 1
				#lines.append({'from': place1, 'to': place2, 'coordinates': [lat1, lng1, placesDict[place2]['lat'], placesDict[place2]['lng']]})

    client.db_close()


	output = {"type":"FeatureCollection","features":[]}

	#for record in records:
		#if scoreDict[record._rid] < 1:
			#continue
		feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
		feature["id"] = record._rid
		#feature["properties"]["name"] = record.title
		#feature["properties"]["cat"] = record.cat_1
		#feature["properties"]["score"] = scoreDict[record._rid]
		feature["geometry"]["coordinates"] = [record.lat, record.lng]

		output["features"].append(feature)


	#output["lines"] = lines

	#q.put('idle')
	return json.dumps(output)

filter_database()

#if __name__ == "__main__":
#    app.run(host='0.0.0.0',port=4000,debug=True,threaded=True)