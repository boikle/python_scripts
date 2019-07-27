'''
Bulk lidar processing script
'''

import os

DATA_DIR = '~/Desktop/lidar_processing/data/'

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
            os.system('file ' + file_path)

# Delete old tiles
delete_tiles()

# Create lidar tiles
create_lidar_tiles()
