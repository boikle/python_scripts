## NSIDC Sea Ice Extent Post-Processing Script ##
Description: NSIDC Sea Ice Index data was downloaded for sea ice extent polygons. Spatial data was downloaded as monthly median sea ice extent, each provided in a zip file. 

NSIDC Sea Ice Index data in the form of sea ice extent polygons, required post-processing to be in a format which could be imported into a Nunaliit Atlas. The following script processes the data from hundreds of multi-feature shape files (stored in zip files) into a single collection of features which are dissolved based on an added date and source fields. 

### Processing Steps ###
```
╔═════════════════╗
║   Directory of  ║
║ zip shape files ║
╚═════════════════╝
        ▼
╔═════════════════╗
║    Unzip all    ║
║   shape files   ║
╚═════════════════╝
        ▼
╔═════════════════╗
║   Add source    ║
║  & date fields  ║
╚═════════════════╝
        ▼
╔═════════════════╗
║  Convert each   ║
║ shape file to   ║
║ a GeoJSON using ║
║    EPSG:4326    ║
╚═════════════════╝
        ▼
╔═════════════════╗
║ Dissolve multi- ║
║ features into   ║
║  one polygon    ║
║ representing a  ║
║ monthly sea ice ║
║     extent      ║
╚═════════════════╝
        ▼
╔═════════════════╗
║ Merge GeoJSON   ║
║ files into a    ║
║ single GeoJSON  ║
╚═════════════════╝
```
### Prerequisites ###
* GDAL, available [here](http://www.gdal.org/).
