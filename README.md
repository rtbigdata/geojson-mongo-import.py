# geojson-mongo-import.py
Import GeoJSON file into MongoDB using Python

Before running ensure you have the PyMongo module installed:

`pip install pymongo`

Example usage:

`python geojson-mongo-import.py points.geojson points`

Given an input file named "points.geojson" having GeoJSON points and destination collection named "points".  This repo includes a "points.geojson" file which is a FeatureCollection of points and a couple of properties including a timestamp.

After importing the GeoJSON file, this script creates a MongoDB [2dsphere](https://docs.mongodb.com/manual/core/2dsphere/) geospatial index on the collection (if the named index does not exist).  It also creates the named database and collection if they do not exist.

Script requires MongoDB 2.4 or higher, and was developed using Python 2.7 and a MongoDB 3.4 server.




