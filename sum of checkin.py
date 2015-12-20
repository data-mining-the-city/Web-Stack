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

db_name = "weibo1"

if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
	client.db_open( db_name, "admin", "admin" )
else:
	print "database does not exist!"
	sys.exit()


result = client.command("SELECT * FROM checkin where time > '2013-01-04 00:00:00' AND time < '2013-12-31 23:59:59' And cat_2 = 'Food/Drinks'")
numRecords = len(result)

numRetrieve = 2000

iterations = int(math.ceil(numRecords/numRetrieve))
print "Number of Records: " + str(numRecords)
print "Number of Iterations: " + str(iterations)

currProgress = 0
progressBreaks = .05

currentRID = "#-1:-1"

voter = []

for i in range(0,366):
	voter.append(0)



for i in range(iterations):


	results = client.command("SELECT FROM checkin WHERE @rid > {} LIMIT {}".format(currentRID, numRetrieve))

	print results[0]._rid

	for record in results:
		time = record.time
		i = int(time.strftime('%j'))
		voter[i] = voter[i]+1


	currentRID = results[-1]._rid

	c = float(i) / float(iterations)


	if c > (currProgress + progressBreaks):
		print "done: " + str(int(c * 100)) + "%"
		currProgress = c

fout = open("./queryRes1.txt", "w")

for j in range(0,366):
		string = str(j) + "\t" + str(voter[j])
		fout.write(string + "\n")

client.db_close()