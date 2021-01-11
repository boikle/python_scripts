# Remove Fields From GeoJSON:
A processing script for removing specified fields from geojson data. 

# Requirements:

* Python 3.6+
* fiona
* tqdm 

# How To Use:
Syntax: `python remove_fields_from_geojson.py <input-file> <list-of-fields>`
Example: `python remove_fields_from_geojson.py cities.geojson "foobar,temp,test"`

# Example Of Transformation:

Input:
```
{
"type": "FeatureCollection",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
{ "type": "Feature", "properties": { "UID": "1", "foo": "bar" }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -100.123456789012345, 50.123456789012345 ], [ -110.123456789012345, 60.123456789012345 ], [ -100.123456789012345, 50.123456789012345 ] ] ] } }
]
}
```

Output with the field 'foo' being removed:
```
{
"type": "FeatureCollection",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
{ "type": "Feature", "properties": { "UID": "1" }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -100.123456789012345, 50.123456789012345 ], [ -110.123456789012345, 60.123456789012345 ], [ -100.123456789012345, 50.123456789012345 ] ] ] } }
]
}
```

