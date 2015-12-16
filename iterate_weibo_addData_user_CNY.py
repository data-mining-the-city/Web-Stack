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
result = client.command("SELECT COUNT(*) FROM User")
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
time1 = datetime.datetime.strptime("2014-01-23 00:00:00", '%Y-%m-%d %H:%M:%S')
time2 = datetime.datetime.strptime("2014-01-30 00:00:00", '%Y-%m-%d %H:%M:%S')
time3 = datetime.datetime.strptime("2014-02-06 00:00:00", '%Y-%m-%d %H:%M:%S')
time4 = datetime.datetime.strptime("2014-02-13 00:00:00", '%Y-%m-%d %H:%M:%S')

for i in range(iterations):

	#get chunk of records, starting with the current one
	results = client.command("SELECT FROM User WHERE @rid > {} AND @version < 41 LIMIT {}".format(currentRID, numRetrieve))

	#print first record received (for troubleshooting)
	print results[0]._rid

	#for each record in chunk
	for record in results:
	       print record.uid
	       if record.uid == "":

			try:
				#check if property exists (to skip records that have already been processed)
				x = record.CNY

				#if property does not exist, it throws a 'AttributeError', causing the following code to run
			except AttributeError:

				#get all checkins for current User record as a list
				checkins = client.command("SELECT expand(out_Checkin) FROM {}".format(record._rid))

				#create three booleans, initialized as False, to store whether checkins occured in the three weeks
				week1 = False
				week2 = False
				week3 = False

				#loop through all checkins
				for checkin in checkins:

					#get time of the checkin (this will come in as a datetime object)
					t = checkin.time

					#if the boolean for the first week is false, check if the current checkin is in that week
					if not week1:
					       if t >= time1 and t < time2:
							#if it is, change that week's boolean to True
						 	#the week will stay true and will not be checked again to save time
							week1 = True

							if not week2:
								if t >= time2 and t < time3:
									week2 = True

									if not week3:
										if t >= time3 and t < time4:
											week3 = True

			#convert three booleans (which can be represented as three digit binary number) to an integer from 0-7
			CNY = ('week1' * 1 * 2**0) + ('week2' * 1 * 2**1) + ('week3' * 1 * 2**2)

			#write the resulting value to the dataset
			client.command("UPDATE {} SET {} = {}".format(record._rid, 'CNY', CNY))

	#set last record in chunk to current record
	currentRID = results[-1]._rid

	#print out progress (for debugging)
	c = float(i) / float(iterations)
	if c > (currProgress + progressBreaks):
		print "done: " + str(int(c * 100)) + "%"
		currProgress = c


client.db_close()
