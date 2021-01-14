import sys
import os
import geopandas as gpd
import geopandas.tools as gdptools
from tqdm import tqdm

def combine_inputs(input_dir):
    combined_data = None

    print("Combining all input data")
    # Check if the input directory exists:
    if os.path.isdir(input_dir):
        for file in tqdm(os.listdir(input_dir)):
            print("Reading input file {}".format(file))
            temp = gpd.read_file(input_dir + '/' + file)

            if combined_data is not None:
                combined_data = combined_data.append(temp)
            else:
                combined_data = temp

    return combined_data


def split_data_by_split_field(input_data, split_field):
    print("Splitting up input data:")
    unique_split_values = input_data[split_field].unique()

    for split_value in tqdm(unique_split_values):
        if isinstance(split_value, str):
            split_data = input_data[input_data[split_field] == split_value]
            split_data.to_file('output/' + split_value + '.geojson', driver='GeoJSON')


def main(inputs_dir, split_data, split_field):

    input_crs = 'epsg:3347'

    # Combine input files into a single input geodataframe
    inputs_df = combine_inputs(inputs_dir)

    # Ensure inputs use correct crs
    inputs_df = inputs_df.to_crs(input_crs)
    print(inputs_df)

    # Read geospatial features used for splitting data
    split_features = gpd.read_file(split_data)
    split_features = split_features.to_crs(input_crs)

    # Create centroids for all input data
    input_centroids = gpd.GeoDataFrame(inputs_df.centroid, geometry=inputs_df.centroid, crs=inputs_df.crs)

    # Intersect split data with input centroids
    intersected_data = gdptools.sjoin(input_centroids, split_features, how='left', op='within')

    inputs_df[split_field] = intersected_data[split_field]
    print(inputs_df)

    split_data_by_split_field(inputs_df, split_field)

if __name__ == "__main__":
    if len(sys.argv) >= 4:
       main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        raise SyntaxError("Invalid number of arguments")