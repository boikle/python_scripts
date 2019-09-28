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
    print('Deleting old classification data ...')
    os.system('rm -r ' + DATA_DIR + 'classified')
    os.system('mkdir ' + DATA_DIR + 'classified')
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
    print('\nGenerating ground tiles ...')
    file_path = DATA_DIR + 'tiles/*.laz'
    ground_path = DATA_DIR + 'ground/'
    os.system('wine ' + LASTOOLS_DIR + 'lasground -i "' + file_path
              + '" -odir ' + ground_path + ' -olaz'
              + ' -cores 4')

def create_height_tiles():
    '''Create Lidar height laz fils'''
    print('\nGenerating height tiles ...')
    file_path = DATA_DIR + 'ground/*.laz'
    height_path = DATA_DIR + 'height/'
    os.system('wine ' + LASTOOLS_DIR + 'lasheight -i "' + file_path
              + '" -drop_below -2 -drop_above 30 -cores 4'
              + ' -odir ' + height_path + ' -olaz')

def classify_height_tiles():
    '''Create Lidar height laz fils'''
    print('\nClassifying height tiles ...')
    file_path = DATA_DIR + 'height/*.laz'
    classified_path = DATA_DIR + 'classified/'
    os.system('wine ' + LASTOOLS_DIR + 'lasclassify -i "' + file_path
              + '" -step 3 -cores 4'
              + ' -odir ' + classified_path + ' -olaz')

def create_dems():
    '''Create Digital Elevation Models for each ground classification'''
    print('\nGenerating dem rasters ...')
    file_path = DATA_DIR + 'ground/*.laz'
    dem_path = DATA_DIR + 'dems/'
    os.system('wine ' + LASTOOLS_DIR + 'las2dem -i "' + file_path
              + '" -odir ' + dem_path + ' -keep_classification 2 -elevation'
              + ' -otif -cores 4')


# Delete old work directories
del_work_dirs()

# Create lidar tiles
create_lidar_tiles()

# Create lidar ground tiles
create_ground_tiles()

# Create lidar height tiles
create_height_tiles()

# Classify height tiles
classify_height_tiles()

# Create dem tiles
create_dems()

# Calculate Elapsed Time:
ELAPSED_TIME = time.time() - START_TIME
print('\nElapsed Time: ' + time.strftime("%H:%M:%S", time.gmtime(ELAPSED_TIME)))
