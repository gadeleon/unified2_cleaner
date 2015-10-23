# Unified2 cleaner

Script that will remove snort unified2 files based on a specified day interval (default: 30).

# Asssumes snort unified2 data is in "/var/log/snort", using the default pretext of unified2 files "snort-unified2", and unified2 files size is 128MB!

You can change the location within `_get_snort_interface_directories(snort_path='/var/log/snort')` and `_get_unified2_file_list(interface_path, unified2_prefix='snort-unified2')`
Hoping future versions will locate and grab this info from your snort.conf file.

# Examples

Evaluate how many files you can delete and space you can reclaim for unified files 30+ days old

`
python do.py --eval
`

Evaluate how many files you can delete and space you reclaim for unified2 files 5+ days old


`
python unified2_cleanup.py -d 5 --eval
`

Delete files 30+ days old

`
python unified2_cleanup.py --purge
`

Delete files 10+ days old

`
python unified2_cleanup.py -d 10 --purge
`

