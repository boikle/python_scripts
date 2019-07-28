'''
Bulk lidar processing script
'''

import os
HOME_DIR = os.getenv("HOME")
DATA_DIR = HOME_DIR + '/Desktop/lidar_processing/data/'
LASTOOLS_DIR = HOME_DIR + '/LAStools/bin/'

def delete_tiles():
    '''Delete old tiles'''
    print('Deleting old tile data ...')
    os.system('rm -r ' + DATA_DIR + 'tiles')
    os.system('mkdir ' + DATA_DIR + 'tiles')

def create_lidar_tiles():
    '''Create lidar tiles for each laz file'''
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR, filename)
            tile_path = os.path.join(DATA_DIR + 'tiles/', filename)
            os.system('wine ' + LASTOOLS_DIR + 'lastile -i "' + file_path
                      + '" -tile_size 500 -buffer 25 -o ' + tile_path)

# Delete old tiles
delete_tiles()

# Create lidar tiles
create_lidar_tiles()
