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
    def __init__(self):
        self.outDriver = gdal.GetDriverByName("GTiff")

    def _outputRaster(self, inputArray, outputRaster):
        print("Outputing raster result...")
        outputRaster = self.outDriver.Create(str(outputRaster), self.rows, self.cols, 1, gdal.GDT_Float32)
        
        # write NBRarray to output file
        outputRaster.GetRasterBand(1).WriteArray(inputArray)
        outputRaster.SetGeoTransform(self.geoTransform)
        outputRaster.SetProjection(self.projection)

        # Close output raster
        outputRaster = None

    def _getImgSpecs(self, raster):
        print("Getting Image Specifications ...")
        inputRaster = gdal.Open(raster)
        self.geoTransform = inputRaster.GetGeoTransform()
        self.projection = inputRaster.GetProjection()
        [self.cols,self.rows] = inputRaster.ReadAsArray().shape

        # Close input raster
        inputRaster = None

class nbr(burnScarAnalysis):
    def __init__(self, red, nir, output):
        burnScarAnalysis.__init__(self)
        self.redBand = gdal.Open(red)
        self.redBandArray = self.redBand.ReadAsArray()
        self.nirBand = gdal.Open(nir)
        self.nirBandArray = self.nirBand.ReadAsArray()
        self.outputRaster = output

        # Retrieve Image specifications
        burnScarAnalysis._getImgSpecs(self, red)

        # Create mask for imagery
        self.maskValue = -9999
        self._createMask()

        # Create NBR
        self._createNBR()

        # Close Data-sets
        self._closeDatasets()

    def _closeDatasets(self):
        print("Closing Datasets ...")
        self.redBand = None
        self.nirBand = None

    # Create a mask indicating invalid pixels
    # - Mask out invalid Landsat 8 surface reflectance values (< 0 | > 10000)
    # - Mask out when denominator equals 0
    def _createMask(self):
        print("Creating Mask ...")
        self.mask = numpy.where((self.redBandArray < 0) 
        | (self.nirBandArray < 0) 
        | (self.redBandArray > 10000) 
        | (self.nirBandArray > 10000) 
        | (self.redBandArray + self.nirBandArray == 0), 0, 1)

    # Normalized Burn Ratio 
    # NBR = (Red - NIR)/(Red + NIR)
    def _createNBR(self):
        print("Creating Normalized Burn Ratio ...")
        NBRArray = numpy.choose(self.mask,(self.maskValue, 
        (self.redBandArray - self.nirBandArray)/
        (self.redBandArray + self.nirBandArray)))
        self._outputRaster(NBRArray,self.outputRaster)

class difference(burnScarAnalysis):
    def __init__(self, preNBR, postNBR, output):
        burnScarAnalysis.__init__(self)
        self.preNBR = gdal.Open(preNBR)
        self.preNBRArray = self.preNBR.ReadAsArray()
        self.postNBR = gdal.Open(postNBR)
        self.postNBRArray = self.postNBR.ReadAsArray()
        self.outputRaster = output

        # Retrieve Image specifications
        burnScarAnalysis._getImgSpecs(self, preNBR)

        # If raster extents match create NBR Difference Raster
        if (self._matchingExtents()):
            self._createDifference()
            self._closeDatasets()

    def _matchingExtents(self):
        preGT = self.preNBR.GetGeoTransform()
        postGT = self.postNBR.GetGeoTransform()

        if( preGT != postGT ):
            print("Error: Extents of Pre and Post NBR rasters don't match")
            return False
        else: 
            return True

    def _closeDatasets(self):
        print("Closing Datasets ...")
        self.preNBR = None
        self.postNBR = None

    # Normalized Burn Ratio Difference
    # NBRDifference = (pre-fire-nbr - post-fire-nbr)
    def _createDifference(self):
        print("Creating Normalized Burn Ratio Difference Raster...")
        NBRDifferenceArray = (self.preNBRArray - self.postNBRArray)
        self._outputRaster(NBRDifferenceArray,self.outputRaster)