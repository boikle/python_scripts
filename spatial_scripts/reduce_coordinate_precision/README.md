# Reduce Coordinate Precision in GeoJSON:
A processing script for reducing the coordinate precision of coordinates in a geojson's feature geometry. 

# Requirements:

* Python 3.6+
* fiona
* shapely
* tqdm 

# How To Use:
Syntax: `python reduce_coordinate_precision.py <input-file> <list-of-fields>`
Example: `python reduce_coordinate_precision.py cities.geojson 5`

# Example Of Transformation:

Input:
```
{
"type": "FeatureCollection",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
{ "type": "Feature", "properties": { "UID": "1" }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -100.123456789012345, 50.123456789012345 ], [ -110.123456789012345, 60.123456789012345 ], [ -100.123456789012345, 50.123456789012345 ] ] ] } }
]
}
```

Output with a reduced coorinate precision of 5:
```
{
"type": "FeatureCollection",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
{ "type": "Feature", "properties": { "UID": "1" }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -100.12345, 50.12345 ], [ -110.12345, 60.12345 ], [ -100.12345, 50.12345 ] ] ] } }
]
}
```

