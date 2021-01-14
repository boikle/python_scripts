"""
Geospatial script for combining a collection of input data, and then splitting
the combined data based on field in a specified split feature dataset.
"""
import sys
import os
import geopandas as gpd
import geopandas.tools as gdptools
from tqdm import tqdm

INPUT_CRS = 'epsg:3347'


def combine_inputs(input_dir):
    """
    Combine a directory of spatial data into a single geodataframe

    Attribute:
    -------------
    :param input_dir {string} - Path to the input directory.

    Returns:
    -------------
    combined_data {GeoDataFrame} - A GeoDataFrame containing the combined input data
    """
    combined_data = None

    print("Combining all input data")
    # Check if the input directory exists:
    if os.path.isdir(input_dir):
        for file in tqdm(os.listdir(input_dir)):
            file_ext = file.split('.')[-1]
            if file_ext == 'shp' or file_ext == 'geojson':
                print("\nReading input file {}".format(file))
                temp = gpd.read_file(input_dir + '/' + file)
                temp = temp.to_crs(INPUT_CRS)

                if combined_data is not None:
                    combined_data = combined_data.append(temp)
                else:
                    combined_data = temp

    return combined_data


def split_data_by_split_field(input_data, split_field):
    """
    Split combined input data by intersecting it with the split features, and breaking up
    the input data based on the specified field in the split dataset.

    Attributes:
    -------------
    :param input_data {GeoDataFrame} - GeoDataFrame containing the combined collection of input data
    :param split_field {string} - Name of field used to split of GeoDataFrame into separate GeoJSON files
    """
    print("Splitting up input data:")
    unique_split_values = input_data[split_field].unique()

    for split_value in tqdm(unique_split_values):
        if isinstance(split_value, str):
            split_data = input_data[input_data[split_field] == split_value]
            split_data.to_file('output/' + split_value + '.geojson', driver='GeoJSON')


def main(inputs_dir, split_data, split_field):
    """
    Entry point for merge and split processing script

    Attributes:
    ------------
    :param inputs_dir {string} - Path to the directory containing input data
    :param split_data {string} - Path to the geospatial file used for splitting the combined input data
    :param split_field {string} - Field name in split data used for dividing up combined input data
    """
    # Combine input files into a single input geodataframe
    inputs_df = combine_inputs(inputs_dir)

    # Read geospatial features used for splitting data
    split_features = gpd.read_file(split_data)
    split_features = split_features.to_crs(INPUT_CRS)

    # Create centroids for all input data
    input_centroids = gpd.GeoDataFrame(inputs_df.centroid, geometry=inputs_df.centroid, crs=inputs_df.crs)

    # Intersect split data with input centroids
    intersected_data = gdptools.sjoin(input_centroids, split_features, how='left', op='within')

    # Copy intersected split field value to input dataframe
    inputs_df[split_field] = intersected_data[split_field]

    # Split input data used split data
    split_data_by_split_field(inputs_df, split_field)


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        raise SyntaxError("Invalid number of arguments")
