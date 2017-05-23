#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bulk import GeoJSON file into MongoDB
# Note: bulk operations require MongoDB 3.2 or higher
#
# example usage:
# given an input file named "points.geojson" having GeoJSON points
# and destination collection named "points"
#
# python geojson-mongo-import.py points.geojson points
#
#

import sys, json
from datetime import datetime
from pymongo import MongoClient, GEOSPHERE
from pymongo.errors import (PyMongoError, BulkWriteError)

inputfile = sys.argv[1]
to_collection = sys.argv[2]

with open(inputfile,'r') as f:
  geojson = json.loads(f.read())

client = MongoClient('mongodb://localhost:27017/')
db = client['geospatial']
collection = db[to_collection]

# create 2dsphere index and initialize unordered bulk insert
collection.create_index([("geometry", GEOSPHERE)])
bulk = collection.initialize_unordered_bulk_op()

for feature in geojson['features']:
  # Note: comment out next two lines if input file does not contain timestamp field having proper format
  # timestamp = feature['properties']['timestamp']
  # feature['properties']['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

  # append to bulk insert list
  bulk.insert(feature)

# execute bulk operation to the DB
try:
  result = bulk.execute()
  print "Number of Features successully inserted:", result["nInserted"]
except BulkWriteError as bwe:
  nInserted = bwe.details["nInserted"]
  errMsg = bwe.details["writeErrors"]
  print "Errors encountered inserting features"
  print "Number of Features successully inserted:", nInserted
  print "The following errors were found:"
  for item in errMsg:
    print "Index of feature:", item["index"]
    print "Error code:", item["code"]
    print "Message (truncated due to data length):", item["errmsg"][0:120], "..."


