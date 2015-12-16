#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
import urllib
import urllib2
import json
import types
import datetime

import pyorient


client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "password")

db_name = "weibo"

if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
	client.db_open( db_name, "admin", "admin" )
else:
	print "database does not exist!"
	sys.exit()


#get total number of records in the User class
result = client.command("SELECT COUNT(*) FROM Checkin")
numRecords = result[0].COUNT

#number of records to retrieve at a time (chunks)
numRetrieve = 1000

#get number of iterations (total number of times to retrieve chunks of records)
iterations = int(math.ceil(numRecords/numRetrieve))
print "Number of Records: " + str(numRecords)
print "Number of Iterations: " + str(iterations)

currProgress = 0
progressBreaks = .05

#set current record to first record
currentRID = "#-1:-1"

#time breaks
#time1 = datetime.datetime.strptime("2014-01-23 00:00:00", '%Y-%m-%d %H:%M:%S')
#time2 = datetime.datetime.strptime("2014-02-13 00:00:00", '%Y-%m-%d %H:%M:%S')

for i in range(iterations):

	#get chunk of records, starting with the current one
	results = client.command("SELECT * FROM Checkin WHERE @rid > {} AND time < '2014-01-23 00:00:00' OR time > '2014-02-13 00:00:00' LIMIT {}".format(currentRID, numRetrieve))

	#print first record received (for troubleshooting)
	print results[0]._rid

	#for each record in chunk
	for record in results:
	       print record.cid
			   #write the resulting value to the dataset
	       client.command("DELETE EDGE WHERE cid = {}".format(record.cid))
				#UPDATE {} SET {} = {}".format(record._rid, 'CNY', CNY))

	#set last record in chunk to current record
	currentRID = results[-1]._rid

	#print out progress (for debugging)
	#c = float(i) / float(iterations)
	#if c > (currProgress + progressBreaks):
		#print "done: " + str(int(c * 100)) + "%"
		#currProgress = c


client.db_close()
