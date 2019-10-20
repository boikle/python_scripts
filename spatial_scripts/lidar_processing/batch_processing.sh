#!/bin/bash
# batch processing of files
batchsize=1
count=0
for filename in unprocessed/*.laz; do
	file=$(basename "$filename" .laz)
	mv $filename data/.
	echo Moving $filename
	((count++))
	if [ $count -eq $batchsize ];
	then
		python3 ~/workspace/python_scripts/spatial_scripts/lidar_processing/lidar_processing.py
		count=0
		mv  data/*.laz processed/.
		/usr/bin/gdal_merge.py -a_nodata -9999 -ot Float32 -o dtms/$file.tif -of GTiff data/dtms/*.tif 
		mv -f data/dtms/* processed/dtms/.
		echo Starting Next Batch
	fi
done
echo Finished Batch Processing
