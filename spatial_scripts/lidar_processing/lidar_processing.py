'''
Bulk lidar processing script
'''

import os
import time
HOME_DIR = os.getenv("HOME")
DATA_DIR = HOME_DIR + '/Desktop/lidar_processing/data/'
LASTOOLS_DIR = HOME_DIR + '/LAStools/bin/'
TILE_SIZE = '200'
BUFFER = '25'
START_TIME = time.time()

def del_work_dirs():
    '''Delete old work directories'''
    print('Deleting old tile data ...')
    os.system('rm -r ' + DATA_DIR + 'tiles')
    os.system('mkdir ' + DATA_DIR + 'tiles')
    print('Deleting old ground data ...')
    os.system('rm -r ' + DATA_DIR + 'ground')
    os.system('mkdir ' + DATA_DIR + 'ground')
    print('Deleting old height data ...')
    os.system('rm -r ' + DATA_DIR + 'height')
    os.system('mkdir ' + DATA_DIR + 'height')
    print('Deleting old dem rasters ...')
    os.system('rm -r ' + DATA_DIR + 'dems')
    os.system('mkdir ' + DATA_DIR + 'dems')


def create_lidar_tiles():
    '''Create lidar tiles for each laz file'''
    print('\nGenerating lidar tiles ...')
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR, filename)
            tile_path = os.path.join(DATA_DIR + 'tiles/', filename)
            os.system('wine ' + LASTOOLS_DIR + 'lastile -i "' + file_path
                      + '" -tile_size ' + TILE_SIZE
                      + ' -buffer ' + BUFFER
                      + ' -epsg 2953 '
                      + ' -cores 4 '
                      + ' -o ' + tile_path)

def create_ground_tiles():
    '''Create Lidar ground laz fils'''
    print('\nGenerating ground classifications of lidar data ...')
    for filename in os.listdir(DATA_DIR + 'tiles/'):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR + 'tiles/', filename)
            ground_path = os.path.join(DATA_DIR + 'ground/')
            os.system('wine ' + LASTOOLS_DIR + 'lasground -i "' + file_path
                      + '" -odir ' + ground_path + ' -olaz')

def create_height_tiles():
    '''Create Lidar height laz fils'''
    print('\nGenerating height classifications of lidar data ...')
    for filename in os.listdir(DATA_DIR + 'tiles/'):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR + 'ground/', filename)
            height_path = os.path.join(DATA_DIR + 'height/')
            os.system('wine ' + LASTOOLS_DIR + 'lasheight -i "' + file_path
                      + '" -drop_below -2 -drop_above 30 '
                      + ' -odir ' + height_path + ' -olaz')

def create_dems():
    '''Create Digital Elevation Models for each ground classification'''
    print('\nGenerating dem rasters ...')
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

# Create lidar ground tiles
create_ground_tiles()

# Create lidar height tiles
create_height_tiles()

# Create dem tiles
create_dems()

# Calculate Elapsed Time:
ELAPSED_TIME = time.time() - START_TIME
print('\nElapsed Time: ' + time.strftime("%H:%M:%S", time.gmtime(ELAPSED_TIME)))
