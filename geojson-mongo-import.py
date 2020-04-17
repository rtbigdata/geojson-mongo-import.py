#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bulk import GeoJSON file into MongoDB
# Note: bulk operations require MongoDB 3.2 or higher
#
# example usage:
# given an input file named "points.geojson" having GeoJSON points
# into destination DB "geospatial" and collection named "points"
#
# python geojson-mongo-import.py -f points.geojson -d geospatial -c points
#
#

import argparse, urllib, json
from datetime import datetime
from pymongo import MongoClient, GEOSPHERE
from pymongo.errors import (PyMongoError, BulkWriteError)

parser = argparse.ArgumentParser(description='Bulk import GeoJSON file into MongoDB')
parser.add_argument('-f', required=True, help='input file')
parser.add_argument('-s', default='localhost', help='target server name (default is localhost)')
parser.add_argument('-port', default='27017', help='server port (default is 27017)')
parser.add_argument('-d', required=True, help='target database name')
parser.add_argument('-c', required=True, help='target collection to insert to')
parser.add_argument('-u', help='username (optional)')
parser.add_argument('-p', help='password (optional)')
args = parser.parse_args()

inputfile = args.f
to_collection = args.c
to_database = args.d
to_server = args.s
to_port = args.port
db_user = args.u

if db_user is None:
  uri = 'mongodb://' + to_server + ':' + to_port +'/'
else:
  db_password = urllib.quote_plus(args.p)
  uri = 'mongodb://' + db_user + ':' + db_password + '@' + to_server + ':' + to_port +'/' + to_database

with open(inputfile,'r') as f:
  geojson = json.loads(f.read())

client = MongoClient(uri)
db = client[to_database]
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
  print("Number of Features successully inserted:", result["nInserted"])
except BulkWriteError as bwe:
  nInserted = bwe.details["nInserted"]
  errMsg = bwe.details["writeErrors"]
  print("Errors encountered inserting features")
  print("Number of Features successully inserted:", nInserted)
  print("The following errors were found:")
  for item in errMsg:
    print("Index of feature:", item["index"])
    print("Error code:", item["code"])
    print("Message (truncated due to data length):", item["errmsg"][0:120], "...")


