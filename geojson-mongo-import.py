#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from pymongo import MongoClient, GEOSPHERE

with open('points.geojson','r') as f:
  geojson = json.loads(f.read())

client = MongoClient('mongodb://localhost:27017/')
db = client['geospatial']
collection = db['points']

for feature in geojson['features']:
  timestamp = feature['properties']['timestamp']
  feature['properties']['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
  collection.insert_one(feature)

collection.create_index([("geometry", GEOSPHERE)])

