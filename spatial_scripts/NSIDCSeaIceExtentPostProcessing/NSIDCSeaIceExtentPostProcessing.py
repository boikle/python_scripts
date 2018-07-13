# Name: SeaIceDataProcessing.py
# --------------------------------------------
# Description: NSIDC Sea Ice Index data in the form of sea ice extent polygons, required 
# post-processing to be in a format which can be imported into a Nunaliit Atlas. The following 
# script massages the data from hundreds of multi feature shape files (stored in zip files) 
# into a single collection of features which are dissolved based on added date and source information. 
# ---------------------------------------------
# How to use the script: Simply update the NSIDCDATADIR directory string which contains the downloaded 
# sea ice index (polygon extents) zip files, and then run the script using Python 3. 

from osgeo import ogr
import os

# This needs to be updated to the location of NSIDC Data Directory
NSIDCDATADIR = "~/NSIDC_Sea_Ice_Extent_Data/"

def unzipFiles():
    # root = the current directory path starting at NSIDCDATADIR
    # dirs = an array of directory names
    # files = an array of files names 
    print("Unzipping NSIDC Sea Ice Extent Data... ")
    for root, dirs, files in os.walk(NSIDCDATADIR):
        for file in files:
            if file[-4:] == ".zip":
                if os.path.isdir(os.path.join(root, file[:-4])):
                    #remove old directory first if it already exists
                    os.system("rm -r " + os.path.join(root, file[:-4]))

                # unzip file into a new directory
                os.system("unzip " + os.path.join(root, file) + " -d " + os.path.join(root, file[:-4])) 

    print("Extracting Data - Complete\n")

# Add an empty date and source field to the sea ice extent features
def addFields( filename ):
    dataSource = ogr.Open(filename, 1)
    layer = dataSource.GetLayer()
    layerDefinition = layer.GetLayerDefn()

    date_field = ogr.FieldDefn('date',ogr.OFTString)
    date_field.SetWidth(254)
    layer.CreateField(date_field)
    
    source_field = ogr.FieldDefn('source',ogr.OFTString)
    source_field.SetWidth(254)
    layer.CreateField(source_field)

    # Close data source
    dataSource = None

# Set the source information for each feature
def setSourceFieldValue( filename ):
    dataSource = ogr.Open(filename, update=True)
    layer = dataSource.GetLayer()
    feature = layer.GetNextFeature()
        
    while feature:
        feature.SetField("source", "Fetterer, F., K. Knowles, W. Meier, M. Savoie, and A. K. Windnagel. 2017, updated daily. Sea Ice Index, Version 3. Boulder, Colorado USA. NSIDC: National Snow and Ice Data Center. doi: https://doi.org/10.7265/N5K072F8")
        layer.SetFeature(feature)
        feature = layer.GetNextFeature()
    
    # Close data source
    dataSource = None

# Set the date value for each feature
def setYearFieldValue( filename, year, month ):
    dataSource = ogr.Open(filename, update=True)
    layer = dataSource.GetLayer()
    feature = layer.GetNextFeature()
        
    while feature:
        feature.SetField("date", year + "-" + month)
        layer.SetFeature(feature)
        feature = layer.GetNextFeature()
            
    # Close data source
    dataSource = None

def escapeTableName( tableName ):
    return "'" + tableName + "'"

def mergeGeoJsonFiles():
    print("Merging geojson files ...", end="")
    catfile = "nsidc_data.geojson"
    tempfile = "temp.geojson"

    # Delete cat file if it already exists
    if os.path.exists(os.path.join(NSIDCDATADIR, catfile)):
        os.system("rm " + os.path.join(NSIDCDATADIR, catfile))
    
    ## Create new cat file
    os.system("touch " + os.path.join(NSIDCDATADIR, catfile))
    emptyFile = True

    for root, dirs, files in os.walk(NSIDCDATADIR):
        for file in files:
            if file[-18:] == "_dissolved.geojson":
                print(".", end='', flush=True)
                if emptyFile: 
                    os.system("head -n -2 " + os.path.join(root, file) + " >> " + os.path.join(NSIDCDATADIR, catfile))
                    emptyFile = False
                else:
                    os.system("echo ',' >> " + os.path.join(NSIDCDATADIR, catfile))
                    os.system("head -n -2 " + os.path.join(root, file) + " > " + os.path.join(NSIDCDATADIR, tempfile))
                    os.system("tail -n +6 " + os.path.join(NSIDCDATADIR, tempfile) + " >> " + os.path.join(NSIDCDATADIR, catfile))
                    os.system("rm " + os.path.join(NSIDCDATADIR, tempfile))

    # Add closing array brace and closing object bracket
    os.system("echo ']}' >> " + os.path.join(NSIDCDATADIR, catfile))
    print("\nFinished merging data")

# Unzip all NSIDC Data zip files
unzipFiles()

# Loop through all shape files and add a date column
# then transform the SRS to EPSG:4326 and then
# dissolve feature data based on new date and source fields
print("Massaging shape file data ...", end="")
for root, dirs, files in os.walk(NSIDCDATADIR):
    for file in files:
        if file[-4:] == ".shp":
            print(".",end="", flush=True)
            year = file[9:13]
            month = file[13:15]

            addFields(os.path.join(root, file))
            setSourceFieldValue(os.path.join(root, file))
            setYearFieldValue(os.path.join(root, file), year, month)

            geojsonFileName = os.path.join(root, file[:-4]) + '_epsg4326.geojson'

            # Transform shape file into a EPSG:4326 and save the file as a geojson
            os.system('ogr2ogr -f GeoJSON -t_srs EPSG:4326 ' + geojsonFileName + ' ' +  os.path.join(root, file))

            # Dissolve each geojson file
            os.system('ogr2ogr -f GeoJSON ' + geojsonFileName[:-8] + '_dissolved.geojson ' + geojsonFileName + ' -dialect sqlite -sql "SELECT date,source, ST_Collect(geometry) as geometry FROM OGRGeoJSON GROUP BY date,source"')

print("\nFinished massaging data")

# merging geojson files into a single geojson file for importing into Nunaliit
mergeGeoJsonFiles()