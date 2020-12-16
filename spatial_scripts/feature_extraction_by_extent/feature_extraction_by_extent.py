"""
A geospatial script which extracts input features which only intersect with the
bounding box of numerous extent features.
"""
import os
import fiona
import shapely.geometry


def extract_features_by_extent(input_features, extent_features):
    """
    Extract input features contained within the bounding box of the extent features
    :param input_features: fiona collecion of input geospatial features
    :param extent_features: fiona collection of extent geospatial features
    """
    if __name__ == '__main__':
        bounds = extent_features.bounds
        bbox = shapely.geometry.box(bounds[0], bounds[1], bounds[2], bounds[3], ccw=True)
        output_file = extent_features.name + '_' + input_features.name + '.geojson'

        # Iterate through input features and output intersecting features
        with fiona.open(output_file, 'w', driver='GeoJSON', crs=input_features.crs, schema=input_features.schema) as output:
            print("Iterating through input geospatial features...")
            for elem in input_features:
                geom = shapely.geometry.shape(elem['geometry'])
                if geom.intersects(bbox):
                    output.write({
                        'geometry': shapely.geometry.mapping(geom),
                        'properties': elem['properties']
                    })

        print("Finished exporting " + output_file)


def main():
    """
    Entry point of feature extraction script
    """
    extents = 'data/extents/'
    input_data = 'data/input/MS.geojson'

    print("Opening input data...")
    with fiona.open(input_data) as input_features:

        # Loop through sample files
        for file in os.listdir(extents):
            print("\nOpening extent file " + file)
            extent = fiona.open(extents + file, 'r')

            print("Extracting input features in extent's bounding box")
            extract_features_by_extent(input_features, extent)


if __name__ == '__main__':
    main()
