# Script Name: downloadNSIDCSeaIceExtentData.sh
# Description: Downlods all Sea Ice Extent shapefile polygon data zip files from NSIDC  

# Remove old data if it exists
rm -r ./sidads.colorado.edu/

# Get all sea ice index polygon data from NSIDC
wget -r -A "*_polygon_v3.0.zip" ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/monthly/shapefiles/shp_extent/
