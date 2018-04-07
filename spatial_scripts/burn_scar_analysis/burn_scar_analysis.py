import sys

try:
    from osgeo import gdal
except:
    sys.exit("Error: can't find required gdal module")

try:
    import numpy
except:
    sys.exit("Error: can't find required numpy module")


# Define imagery files
july_band5 = "../data/LC08_L1TP_20170705_01_T1_sr_band5_merged.tif"
july_band7 = "../data/LC08_L1TP_20170705_01_T1_sr_band7_merged.tif"
# aug_band5 = "../data/LC08_L1TP_20170822_01_T1_sr_band5_merged.tif"
# aug_band7 = "../data/LC08_L1TP_20170822_01_T1_sr_band7_merged.tif"

# Perform Normalized Burn Ratio on imagery (for both time periods). 

rasterJulyBand5 = gdal.Open(july_band5)
rasterJulyBand5Array = rasterJulyBand5.ReadAsArray()

rasterJulyBand7 = gdal.Open(july_band7)
rasterJulyBand7Array = rasterJulyBand7.ReadAsArray()

# Pre-fire NBR
julyNBR = (rasterJulyBand5Array - rasterJulyBand7Array)/(rasterJulyBand5Array + rasterJulyBand7Array)

#collect information about file
[cols,rows] = rasterJulyBand5Array.shape
trans = rasterJulyBand5.GetGeoTransform()
proj = rasterJulyBand5.GetProjection()

outputFileName = "../data/nbr_july2017.tif"

#create an output file
outdriver = gdal.GetDriverByName("GTiff")
outdata = outdriver.Create(str(outputFileName), rows, cols, 1, gdal.GDT_Float32)

#write the array to the file
outdata.GetRasterBand(1).WriteArray(julyNBR)

#georeference the image
outdata.SetGeoTransform(trans)

#Set projection information
outdata.SetProjection(proj)

# Close datasets
rasterJulyBand5 = None
rasterJulyBand7 = None
outdata = None
# Perform Change detection by calculating difference between both normalized burn ratios from the previous step. 
# difference = early nbr - late nbr