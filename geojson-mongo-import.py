#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import GeoJSON file into MongoDB
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

inputfile = sys.argv[1]
to_collection = sys.argv[2]

with open(inputfile,'r') as f:
  geojson = json.loads(f.read())

client = MongoClient('mongodb://localhost:27017/')
db = client['geospatial']
collection = db[to_collection]

for feature in geojson['features']:
  # Note: comment out the next two lines if your input file does not have a timestamp field in properties
  timestamp = feature['properties']['timestamp']
  feature['properties']['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
  collection.insert_one(feature)

collection.create_index([("geometry", GEOSPHERE)])

