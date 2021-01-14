# Merge and Split 
A simple python script for combining a collection of geospatial data (merge)
and dividing that collection of data based on a specified splitting feature
(e.g. a collection of polygons).

## Script Workflow:

1. Collection of Spatial Input Files (GeoJSON or Shape) are combined into a single GeoDataFrame
2. Combined GeoDataFrame is then converted into Centroids
3. Centroids are intersected with Geospatial features used for splitting
4. Split field from the joined centroid data is then copied to original GeoDataFrame
5. GeoDataFrame is exported into separate GeoJSON files based on the split field.

## Prerequisites:

* Python 3
* geopandas
* pygeos
* tqdm

## How To Use:

* Syntax: `python merge_and_split.py <input-files-dir> <file-for-spliting> <field-for-splitting>`
* Example: `python merge_and_split.py data\myinputfiles data\splitfile.shp mysplitfield`