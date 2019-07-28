'''
Bulk lidar processing script
'''

import os
HOME_DIR = os.getenv("HOME")
DATA_DIR = HOME_DIR + '/Desktop/lidar_processing/data/'
LASTOOLS_DIR = HOME_DIR + '/LAStools/bin/'

def del_work_dirs():
    '''Delete old work directories'''
    print('Deleting old tile data ...')
    os.system('rm -r ' + DATA_DIR + 'tiles')
    os.system('mkdir ' + DATA_DIR + 'tiles')
    print('Deleting old ground data ...')
    os.system('rm -r ' + DATA_DIR + 'ground')
    os.system('mkdir ' + DATA_DIR + 'ground')


def create_lidar_tiles():
    '''Create lidar tiles for each laz file'''
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR, filename)
            tile_path = os.path.join(DATA_DIR + 'tiles/', filename)
            os.system('wine ' + LASTOOLS_DIR + 'lastile -i "' + file_path
                      + '" -tile_size 500 -buffer 25 -o ' + tile_path)

def create_ground_tiles():
    '''Create Lidar ground laz fils'''
    for filename in os.listdir(DATA_DIR + 'tiles/'):
        if filename.endswith('.laz') or filename.endswith('.las'):
            file_path = os.path.join(DATA_DIR + 'tiles/', filename)
            ground_path = os.path.join(DATA_DIR + 'ground/', filename)
            os.system('wine ' + LASTOOLS_DIR + 'lasground -i "' + file_path
                      + '" -o ' + ground_path)

# Delete old work directories
del_work_dirs()

# Create lidar tiles
create_lidar_tiles()

# Create lidar ground files
create_ground_tiles()
