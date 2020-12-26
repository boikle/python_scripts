# Feature Extraction By Extent
A script which extracts data from an input source, based on the extents of spatial data contained in directory

## Prerequisites:

* Shapley
* Fiona

## How To Use Script:

1. Gather extent data and input source data.
2. Update the main function to specify the directory containing extent and input data.
3. Run the python script `python feature_extraction_by_extent.py`

## Example:
A project requires Canadian Open Street Map (OSM) building data to be extracted from areas contained within the extents of road data for specific Canadian cities.

### Project File Structure:
```
├── data
│   ├── extents
│   │   ├── montreal_roads.geojson
│   │   ├── ottawa_roads.geojson
│   │   ├── halifax_roads.geojson
│   │   └── vancover_roads.geojson
│   └── input
│       └── OSM_Buildings.geojson
├── feature_extraction_by_extent.py
└── README.md
```

### How The Script is Updated:

```python
...
def main():
    """
    Entry point of feature extraction script
    """
    extents = 'data/extents/'
    input_data = 'data/input/OSM_Buildings.geojson'

    print("Opening input data...")
    with fiona.open(input_data) as input_features:
...
```

