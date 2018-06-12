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

    def outputRaster(self, inputArray, outputRaster):
        print("Outputing raster result...")
        outputRaster = self.outDriver.Create(str(outputRaster), self.rows, self.cols, 1, gdal.GDT_Float32)
        
        # write NBRarray to output file
        outputRaster.GetRasterBand(1).WriteArray(inputArray)
        outputRaster.SetGeoTransform(self.geoTransform)
        outputRaster.SetProjection(self.projection)

        # Close output raster
        outputRaster = None

    def getImgSpecs(self, raster):
        print("Getting Image Specifications ...")
        inputRaster = gdal.Open(raster)
        self.geoTransform = inputRaster.GetGeoTransform()
        self.projection = inputRaster.GetProjection()
        [self.cols,self.rows] = inputRaster.ReadAsArray().shape

        # Close input raster
        inputRaster = None

    def extentsMatch(self, raster1, raster2):
        if( raster1.GetGeoTransform() != raster2.GetGeoTransform() ):
            print("Error: Raster extents don't match")
            return False
        else: 
            return True

class nbr(burnScarAnalysis):
    def __init__(self, **kwargs):
        burnScarAnalysis.__init__(self)
        if kwargs is not None:
            try: 
                self.redBand = gdal.Open(kwargs['red'])
                self.redBandArray = self.redBand.ReadAsArray()
                self.nirBand = gdal.Open(kwargs['nir'])
                self.nirBandArray = self.nirBand.ReadAsArray()
                self.output = kwargs['output']
                # Get image specifications
                burnScarAnalysis.getImgSpecs(self, kwargs['red'])
            except:
                sys.exit("red, nir, and output parameters must be specified.")

            if 'watermask' in kwargs:
                self.waterMask = gdal.Open(kwargs['watermask'])
                
                if ((self.extentsMatch(self.waterMask, self.redBand)) 
                    and (self.extentsMatch(self.waterMask, self.nirBand))):
                    self.waterMaskArray = self.waterMask.ReadAsArray()
                else:
                    print("Warning: Water mask raster extent doesn't match red or nir raster extents")
                    self.waterMaskArray = False
            else:
                self.waterMaskArray = False

        # Create mask for imagery
        self.maskValue = numpy.NaN
        self.createMask()

        # Create NBR
        self.createNBR()

        # Close Data-sets
        print("Closing Datasets ...")
        self.redBand = None
        self.nirBand = None
        self.waterMaskArray = None

    # Create a mask indicating invalid pixels
    # - Mask out waterbocies if water mask is provided
    # - Mask out invalid Landsat 8 surface reflectance values (< 0 | > 10000)
    # - Mask out when denominator equals 0
    def createMask(self):
        print("Creating Mask ...")
        self.mask = numpy.where((self.waterMaskArray == 1) 
        | (self.redBandArray < 0) 
        | (self.nirBandArray < 0) 
        | (self.redBandArray > 10000) 
        | (self.nirBandArray > 10000) 
        | (self.redBandArray + self.nirBandArray == 0), 0, 1)

    # Normalized Burn Ratio 
    # NBR = (Red - NIR)/(Red + NIR)
    def createNBR(self):
        print("Creating Normalized Burn Ratio ...")
        NBRArray = numpy.choose(self.mask,(self.maskValue, 
        (self.redBandArray - self.nirBandArray)/
        (self.redBandArray + self.nirBandArray)))
        self.outputRaster(NBRArray,self.output)

class difference(burnScarAnalysis):
    def __init__(self, **kwargs):
        burnScarAnalysis.__init__(self)

        if kwargs is not None:
            try: 
                self.preNBR = gdal.Open(kwargs['prenbr'])
                self.preNBRArray = self.preNBR.ReadAsArray()
                self.postNBR = gdal.Open(kwargs['postnbr'])
                self.postNBRArray = self.postNBR.ReadAsArray()
                self.output = kwargs['output']
                # Get image specifications
                burnScarAnalysis.getImgSpecs(self, kwargs['prenbr'])
            except:
                sys.exit("prenbr, postnbr, and output parameters must be specified.")

        # If raster extents match create NBR Difference Raster
        if (self.extentsMatch(self.preNBR,self.postNBR)):
            self.createDifference(self.preNBRArray, self.postNBRArray)

            print("Closing Datasets ...")
            self.preNBR = None
            self.postNBR = None

        else:
            print("Error: Unable to create NBR difference raster.")

    # Normalized Burn Ratio Difference
    # NBRDifference = (pre-fire-nbr - post-fire-nbr)
    def createDifference(self, raster1, raster2):
        print("Creating Normalized Burn Ratio Difference Raster...")
        NBRDifferenceArray = raster1 - raster2
        self.outputRaster(NBRDifferenceArray,self.output)