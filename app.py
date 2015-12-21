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
q = Queue()

def event_stream():
    while True:
        result = q.get()
        yield 'data: %s\n\n' % str(result)

@app.route('/eventSource/')
def sse_source():
    return Response(
            event_stream(), 
            mimetype='text/event-stream' )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getData/")
def getData():
	
	q.put("Yellow Detective is querying the data....")

	lat1 = str(request.args.get('lat1'))
	lng1 = str(request.args.get('lng1'))
	lat2 = str(request.args.get('lat2'))
	lng2 = str(request.args.get('lng2'))

	print "received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"
        q.put("received coordinates: [" + lat1 + ", " + lat2 + "], [" + lng1 + ", " + lng2 + "]"+"         Yellow Detective is querying the data,please be patient......")

	client = pyorient.OrientDB("localhost", 2424)
	session_id = client.connect("root", "f")
	db_name = "weibo"
	db_username = "admin"
	db_password = "admin"

	if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
		client.db_open( db_name, db_username, db_password )
		print db_name + " opened successfully"
	else:
		print "database [" + db_name + "] does not exist! session ending..."
		sys.exit()

	#get checkins
        query = 'SELECT FROM Checkin WHERE lat BETWEEN {} AND {} AND lng BETWEEN {} AND {} AND time BETWEEN "2013-12-03 21:00:00" and "2013-12-04 04:00:00"'
        records = client.command(query.format(lat1, lat2, lng1, lng2))
        
        random.shuffle(records)
	records = records[:60]

        numListings = len(records)
        print 'received ' + str(numListings) + ' Checkins'
    
        uniqueUsers = []
        originPlaces = []
        connectedPlaces = []
        lines = []
        
        output = {"type":"FeatureCollection","features":[],"features1":[],"lines":[]}


        # for each checkin
        for record in records:

           	#get user id
           	user = str(record.out)

           	#skip repeating users
           	if user in uniqueUsers:
          		continue
               	uniqueUsers.append(user)
    	

           	#find connected places
                places = client.command("SELECT * FROM (TRAVERSE out(Checkin) FROM (SELECT * FROM {})) WHERE @class = 'Place'".format(record.out))
                print 'received ' + str(len(places)) + ' connected places from ' + str(record._in)
                q.put("received" + str(len(places)) + "connected places from" + str(record._in))
                #for each connected place, store information of origin and connected place in separate lists
                for place in places:
                   	originPlaces = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
                   	originPlaces["properties"]["text"] = record.text
          		originPlaces["geometry"]["coordinates"] = [record.lat, record.lng]
          		
          		connectedPlaces = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
		        connectedPlaces["properties"]["title"] = place.title
		        connectedPlaces["properties"]["cat"] = place.category_name
		        connectedPlaces["geometry"]["coordinates"] = [place.lat, place.lng]
		        
                        lines.append({'coordinates': [record.lat, record.lng, place.lat, place.lng]})
                   
                        output["features"].append(originPlaces)
                        output["features1"].append(connectedPlaces)
          		
        output["lines"] = lines
        
        q.put("Done! Received " + str(numListings) + " Checkins, Yellow Detective is having a rest")
        
	return json.dumps(output)

   	client.db_close()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True,threaded=True)