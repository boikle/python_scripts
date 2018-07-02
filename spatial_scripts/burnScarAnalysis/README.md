## Burn Scar Analysis ##
A script for performing a burn scar analysis on Landsat 8 satellite imagery. The analysis consists of two steps; 1) calculating the Normalized Burn Ratio (NBR) for the pre-fire and post-fire imagery, and 2) performing a difference of the two NBR results. 

### Prerequisites ###
* GDAL, available [here](http://www.gdal.org/).
* NumPy, available [here](http://www.numpy.org/).

### Configuration Requirements ###
Step 1) Normalized Burn Ratio (nbr) method parameters:
* **red** - The name of the file representing the Red Band of the Landsat 8 imagery (Required). 
* **nir** - The name of the file representing the NIR Band of the Landsat 8 imagery (Required). 
* **output** - The name of the output file for the Normalized Burn Ratio analysis (Required). 
* **watermask** - A raster with cells given the value of 1 representing the location of water bodies (Optional).

Step 2) Difference (difference) method parameters:
* **prenbr** - The name of the file representing the Pre-Fire NBR results (Required). 
* **postnbr** - The name of the file representing the Post-Fire NBR results (Required). 
* **output** - The name of the output file for the NBR difference (Required). 

Note: A consistent spatial extent is expected between the rasters used in both Burn Scar Analysis methods.

### Example: ###
```python
import burnScarAnalysis

# Define imagery and output file locations
preFireRed = "data/preFireRedBand.tif"
preFireNIR = "data/preFireNIRBand.tif"
preFireOutput = "data/preNBROutput.tif"
postFireRed = "data/postFireRedBand.tif"
postFireNIR = "data/postFireNIRBand.tif"
postFireOutput = "data/postNBROutput.tif"
NBRDifferenceOutput = "data/nbrDifference.tif"
waterMask = "data/waterMask.tif"

# Create Normalized Burn Ratio for pre-fire imagery
preFireNBR = burnScarAnalysis.nbr(red=preFireRed, nir=preFireNIR, watermask=waterMask, output=preFireOutput)

# Create Normalized Burn Ratio for post-fire imagery
postFireNBR = burnScarAnalysis.nbr(red=postFireRed, nir=postFireNIR, watermask=waterMask, output=postFireOutput)

# Create NBR difference raster
burnScarAnalysis.difference(prenbr=preFireOutput,postnbr=postFireOutput,output=NBRDifferenceOutput)
```