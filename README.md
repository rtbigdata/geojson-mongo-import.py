# geojson-mongo-import.py
Fast GeoJSON file import into MongoDB using Python

The standard mongoimport tool provided with MongoDB does not recognize GeoJSON files without first editing them manually or running them through a script.  Using this Python program instead of mongoimort takes care of that.  It is assumed that the GeoJSON features will be inserted as individual documents within the target collection.  The other assumption is that your import file is well-formed GeoJSON consisting of a FeatureCollection. This script should work with most standard geometry types supported in MongoDB, including Point, LineString, Polygon, along their respective multipart equivalents, such as MultiPolygon.   

Before running ensure you have the PyMongo module installed:

`pip install pymongo`

Example usage:

`python geojson-mongo-import.py points.geojson points`

Given an input file named "points.geojson" having GeoJSON points and destination collection named "points".  This repo includes a sample "points.geojson" file which is a FeatureCollection of points and a couple of properties including a timestamp.

This script uses bulk write operations which results in nearly a 10x performance boost.  This performance improvement is very noticeable with large GeoJSON files.

Along with importing the GeoJSON file, this script also creates a MongoDB [2dsphere](https://docs.mongodb.com/manual/core/2dsphere/) geospatial index on the collection (if the named index does not exist).  It also creates the named database and collection if they do not exist.

Script requires MongoDB 3.2 or higher (prior releases do not support bulk operations), and was developed using Python 2.7 and a MongoDB 3.4 server.




