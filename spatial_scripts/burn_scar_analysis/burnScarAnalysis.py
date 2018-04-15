import sys

try:
    from osgeo import gdal
except:
    sys.exit("Error: can't find required gdal module")

try:
    import numpy
except:
    sys.exit("Error: can't find required numpy module")

class burnScarAnalysis:
    def __init__(self, *args):
        self.outDriver = gdal.GetDriverByName("GTiff")
        self.preRedBand = gdal.Open(sys.argv[1])
        self.preRedBandArray = self.preRedBand.ReadAsArray()
        self.preNIRBand = gdal.Open(sys.argv[2])
        self.preNIRBandArray = self.preNIRBand.ReadAsArray()
        self.outputFile = sys.argv[3]
        self.maskValue = -9999
    
    def _closeDatasets(self):
        print("Closing Datasets ...")
        self.preRedBand = None
        self.preNIRBand = None

    def _outputRaster(self, nbrArray):
        print("Outputing Normalized Burn Ratio raster ...")
        outputRaster = self.outDriver.Create(str(self.outputFile), self.rows, self.cols, 1, gdal.GDT_Float32)
        
        # write NBRarray to output file
        outputRaster.GetRasterBand(1).WriteArray(nbrArray)
        outputRaster.SetGeoTransform(self.geoTransform)
        outputRaster.SetProjection(self.projection)

        # Close output raster
        outputRaster = None

    def _getImgSpecs(self):
        print("Getting Image Specifications ...")
        self.geoTransform = self.preRedBand.GetGeoTransform()
        self.projection = self.preRedBand.GetProjection()
        [self.cols,self.rows] = self.preRedBandArray.shape

    # Create a mask indicating invalid pixels
    # - Mask out invalid Landsat 8 surface reflectance values (< 0 | > 10000)
    # - Mask out when denominator equals 0
    def _createMask(self):
        print("Creating Mask ...")
        self.mask = numpy.where((self.preRedBandArray < 0) 
        | (self.preNIRBandArray < 0) 
        | (self.preRedBandArray > 10000) 
        | (self.preNIRBandArray > 10000) 
        | (self.preRedBandArray + self.preNIRBandArray == 0), 0, 1)

    # Normalized Burn Ratio 
    # NBR = (Red - NIR)/(Red + NIR)
    def _createNBR(self):
        print("Creating Normalized Burn Ratio ...")
        NBRArray = numpy.choose(self.mask,(self.maskValue, 
        (self.preRedBandArray - self.preNIRBandArray)/
        (self.preRedBandArray + self.preNIRBandArray)))
        self._outputRaster(NBRArray)


burnScar = burnScarAnalysis(sys.argv[1], sys.argv[2], sys.argv[3])
burnScar._getImgSpecs()
burnScar._createMask()
burnScar._createNBR()
burnScar._closeDatasets()
