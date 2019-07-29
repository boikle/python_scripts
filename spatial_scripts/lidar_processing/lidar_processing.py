'''
Bulk lidar processing script
'''

import os
HOME_DIR = os.getenv("HOME")
DATA_DIR = HOME_DIR + '/Desktop/lidar_processing/data/'
LASTOOLS_DIR = HOME_DIR + '/LAStools/bin/'
TILE_SIZE = '250'
BUFFER = '25'

def del_work_dirs():
    '''Delete old work directories'''
    print('Deleting old tile data ...')
    os.system('rm -r ' + DATA_DIR + 'tiles')
    os.system('mkdir ' + DATA_DIR + 'tiles')
    print('Deleting old ground data ...')
    os.system('rm -r ' + DATA_DIR + 'ground')
    os.system('mkdir ' + DATA_DIR + 'ground')
    print('Deleting old dem rasters ...')
    os.system('rm -r ' + DATA_DIR + 'dems')
    os.system('mkdir ' + DATA_DIR + 'dems')


def create_lidar_tiles():
    '''Create lidar tiles for each laz file'''
    print('Generating lidar tiles ...')
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR, filename)
            tile_path = os.path.join(DATA_DIR + 'tiles/', filename)
            os.system('wine ' + LASTOOLS_DIR + 'lastile -i "' + file_path
                      + '" -tile_size ' + TILE_SIZE +' -buffer '
                      + BUFFER + ' -o ' + tile_path)

def create_ground_tiles():
    '''Create Lidar ground laz fils'''
    print('Generating ground classifications of lidar data ...')
    for filename in os.listdir(DATA_DIR + 'tiles/'):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR + 'tiles/', filename)
            ground_path = os.path.join(DATA_DIR + 'ground/', filename)
            os.system('wine ' + LASTOOLS_DIR + 'lasground -i "' + file_path
                      + '" -o ' + ground_path)

def create_dems():
    '''Create Digital Elevation Models for each ground classification'''
    print('Generating dem rasters ...')
    for filename in os.listdir(DATA_DIR + 'ground/'):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR + 'ground/', filename)
            dem_path = os.path.join(DATA_DIR + 'dems/', filename[:-3] + 'tif')
            os.system('wine ' + LASTOOLS_DIR + 'las2dem -i "' + file_path
                      + '" -o ' + dem_path + ' -keep_classification 2 -elevation')


# Delete old work directories
del_work_dirs()

# Create lidar tiles
create_lidar_tiles()

# Create lidar ground files
create_ground_tiles()

# Create dem files
create_dems()
