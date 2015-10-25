'''
Script that will remove unified2 files based on a specified interval.
Compatible with Python 2.6+
'''

import argparse
import datetime
import logging
import sys
import os

# Set up Logger
logger = logging.getLogger('unified2_cleaner')

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Add file handler
fh = logging.FileHandler('uni2log.log')
fh.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s: %(message)s")

# Add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# Add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)

def _get_snort_interface_directories(snort_path='/var/log/snort'):
    '''
    Returns list with absolute path of child folders (interfaces) within snort_path
    '''
    logger.debug('Path of snort_path: {0}'.format(snort_path))
    output = []
    for i in os.listdir(snort_path):
        potential_path = '{0}/{1}'.format(snort_path,i)
        logger.debug('Checking if {0} is a directory'.format(potential_path))
        if os.path.isdir(potential_path):
            logger.debug('{0} is a valid directory'.format(potential_path))
            output.append(potential_path)
            logger.debug('{0} added to list of unified2 paths'.format(potential_path))
    return output


def _get_unified2_file_list(interface_path, unified2_prefix='snort-unified2'):
    '''
    Returns a list of files within an interface folder ex:dag0:32
    '''
    logger.debug('Unified2 prefix: {0}'.format(unified2_prefix))
    output = []
    logger.debug('Checking contents of {0}'.format(interface_path))
    for i in os.listdir(interface_path):
        if i.startswith(unified2_prefix):
            logger.debug('{0} matches unified2_prefix, appending to list of unifed2 files'.format(i))
            output.append(i)
    return output


def _get_epoch(unified2_file):
    '''
    Strips off prefix of a unified2 file and gets the epoch time
    '''
    logger.debug('Splitting file {0}'.format(unified2_file))
    epoch = unified2_file.split('.')[1]
    logger.debug('Extracted epoch time "{0}" from {1}'.format(epoch, unified2_file))
    return int(epoch)


def _days_ago_in_epoch(interval):
    '''
    Get today's date, go back interval days, and convert to epoch time.
    '''
    logger.debug('Interval provided: {0}'.format(str(interval)))
    rotate_day = datetime.datetime.now() - datetime.timedelta(interval)
    logger.debug('Cutoff date: {0}'.format(rotate_day.strftime('%Y-%m-%d %H:%M:%S')))
    epoch_rotate = rotate_day.strftime('%s')
    logger.debug('Cutoff date in Epoch: {0}'.format(epoch_rotate))
    return int(epoch_rotate)


def _is_unified2_too_old(unified2_file, interval):
    '''
    Returns True if Epoch time of unified2_file is less than now - interval days
    '''
    uni_epoch = _get_epoch(unified2_file)
    cutoff = _days_ago_in_epoch(interval)
    if uni_epoch < cutoff:
        logger.debug('{0} is older than {1} days, can be deleted'.format(unified2_file, str(interval)))
        return True
    else:
        logger.debug('{0} is NOT older than {1}, should NOT be deleted'.format(unified2_file, str(interval)))
        return False


def _eligible_files(interval):
    '''
    Returns a list with absolute path of files eligible for deletion based on interval
    '''
    logger.debug('Determining eligible files')
    can_delete = []
    dir_check = _get_snort_interface_directories()
    for i in dir_check:
        uni_check = _get_unified2_file_list(i)
        for x in uni_check:
            age_check = _is_unified2_too_old(x, interval)
            if age_check:
                can_delete.append('{0}/{1}'.format(i,x))
                logger.debug('Added absolute path: {0}/{1}'.format(i,x))
    return can_delete


def _eval_cleanup(interval, unisize=128):
    '''
    Prints number of files that can be deleted and how much space can be saved based on interval
    '''
    if type(interval) != int:
        logger.error('Interval specified is type {0}, must be int'.format(type(interval)))
        sys.exit(1)
    cleanup = _eligible_files(interval)
    print '''
    Number of eligible files: {0}
    Amount of Reclaimable Size: {1}GB
    '''.format(len(cleanup), (len(cleanup)*unisize/1024))


def _cleanup(interval, unisize=128):
    '''
    Deletes files from _eligible_files() list based on interval.
    WARNING: There is no turning back!
    '''
    if type(interval) != int:
        logger.error('Interval specified is type {0}, must be int'.format(type(interval)))
        sys.exit(1)
    confirm = raw_input('WARNING: Type "Y" or "y" to continue and delete files. There is no way to undo this action!: ')
    if confirm.lower() == 'y':
        files = _eligible_files(interval)
        for i in files:
            logger.debug('Removing file {0}'.format(i))
            os.remove(i)
            logger.debug('Removed file: {0}'.format(i))
        logger.info('Files deleted: {0}'.format(len(files)))
        logger.info('Space Reclamed: {0}GB'.format(len(files)*unisize/1024))
        sys.exit(0)
    else:
        logger.info('Not deleting files')
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version',
        version = '%(prog)s 1.0.0')
    parser.add_argument('-d', '--day-interval', type=int,
        nargs='?', const=30,
        help='Any files older than d days ago will be evaluated/deleted \
        (default: 30)')
    parser.add_argument('--eval', action='store_true',
        help='Count the number files you can delete and space you can\
        recover for files d+ days old')
    parser.add_argument('--purge', action='store_true',
        help='Delete files d+ days old.')
    parser.add_argument('--debug', action='store_true',
        help='Turn on debug message')
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if not args.day_interval:
        interval = 30
        logger.debug('interval: {0}'.format(interval))
    elif args.day_interval:
        interval = args.day_interval
    if not args.eval and not args.purge:
        logger.error('Please supply --eval or --purge')
        sys.exit(1)
    if args.eval and args.purge:
        logger.error('Please supply --eval or --purge, not both')
        sys.exit(1)
    if args.eval:
        _eval_cleanup(interval)
    if args.purge:
        _cleanup(interval)


if __name__ == '__main__':
    main()




