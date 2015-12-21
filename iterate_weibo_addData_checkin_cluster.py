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
session_id = client.connect("root", "network.ssl.keyStorePassword")

db_name = "weibo"

if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
	client.db_open( db_name, "admin", "admin" )
else:
	print "database does not exist!"
	sys.exit()


result = client.command("SELECT COUNT(*) FROM Checkin")
numRecords = result[0].COUNT

numRetrieve = 2000

iterations = int(math.ceil(numRecords/numRetrieve))
print "Number of Records: " + str(numRecords)
print "Number of Iterations: " + str(iterations)

currProgress = 0
progressBreaks = .05

currentRID = "#-1:-1"
# currentRID = "#13:4200000"


for i in range(iterations):


	results = client.command("SELECT FROM Checkin WHERE @rid > {} LIMIT {}".format(currentRID, numRetrieve))

	print results[0]._rid

	for record in results:

		try:
			r = record.cluster_id_1
		except AttributeError:
			place = client.command("SELECT * FROM (SELECT expand(in) FROM {})".format(record._rid))

			try:
				client.command("UPDATE {} SET {} = {}".format(record._rid, 'cluster_id_1', place[0].cluster_id_1))
			except:
				print "error: no cluster in place record!"


	currentRID = results[-1]._rid

	c = float(i) / float(iterations)

	if c > (currProgress + progressBreaks):
		print "done: " + str(int(c * 100)) + "%"
		currProgress = c


client.db_close()
