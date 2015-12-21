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

import numpy as np

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets.samples_generator import make_blobs

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

np.random.seed(2)

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "network.ssl.keyStorePassword")

db_name = "weibo"

if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
	client.db_open( db_name, "admin", "admin" )
else:
	print "database does not exist!"
	sys.exit()


result = client.command("SELECT COUNT(*) FROM Place")
numRecords = result[0].COUNT

numRetrieve = 2000

iterations = int(math.ceil(numRecords/numRetrieve))
print "Number of Records: " + str(numRecords)
print "Number of Iterations: " + str(iterations)

currProgress = 0
progressBreaks = .05

currentRID = "#-1:-1"
# currentRID = "#12:4200000"

rids = []
geo = []


for i in range(iterations):
# for i in range(3):

	results = client.command("SELECT FROM Place WHERE @rid > {} LIMIT {}".format(currentRID, numRetrieve))

	print results[0]._rid

	for record in results:

		rids.append(record._rid)
		geo.append([record.lat, record.lng])


	currentRID = results[-1]._rid

	c = float(i) / float(iterations)
	if c > (currProgress + progressBreaks):
		print "done: " + str(int(c * 100)) + "%"
		currProgress = c



X = np.asarray(geo, dtype='float')

###############kmeans################################
#################change the number of clusters(n_clusters)##################
k_means = KMeans(init='k-means++', n_clusters=10, n_init=15)
k_means.fit(X)
k_means_labels = k_means.labels_


##############mean-shifts###########################
#################change the number of clusters(n_clusters)##################
################change the kmeans labels to mbk_means_labels########
mbk = MiniBatchKMeans(init='k-means++', n_clusters=10, batch_size=50, n_init=10, max_no_improvement=10, verbose=0)
mbk.fit(X)
mbk_means_labels = mbk.labels_


for i, rid in enumerate(rids):
	client.command("UPDATE {} SET {} = {}".format(rid, 'cluster_id_1', k_means_labels[i]))
	# print rid
	# sys.exit()



client.db_close()

for i in range(10):
	print "number of places in cluster " + str(i) + ": " + str(list(k_means_labels).count(i))