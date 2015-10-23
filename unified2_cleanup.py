'''
Script that will remove unified2 files based on a specified interval.
Compatible with Python 2.6+
'''

import datetime
import logging
import os

# Set up Logger
logger = logging.getLogger('unified2_cleaner')
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")

# Add formatter to ch
ch.setFormatter(formatter)

# Add ch to logger
logger.addHandler(ch)

def _get_folders(snort_path='/var/log/snort'):
    '''
    Returns list with absolute path of child folders (interfaces) within snort_path
    '''
    logger.debug('Path of snort_path: {0}'.format(snort_path))
    output = []
    for i in os.listdir(snort_path):
        potential_path = '{0}/{1}'.format(snort,i))
        logger.debug('Checking if {0} is a directory'.format(potential_path))
        if os.path.isdir(potential_path):
            logger.debug('{0} is a valid directory'.format(potential_path))
            output.append(potential_path)
            logger.debug('{0} added to list of unified2 paths'.format(potential_path))
    return output

# Debug Section~!
check = _get_folders()
print check