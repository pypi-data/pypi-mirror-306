import argparse
from chipdb_upload.data_upload import run


def main():
    parser = argparse.ArgumentParser('Generates QC metric summary file for available ChIP-seq samples')
    parser.add_argument('-i', '--in_dirs', required=True, nargs='+',
                        help='Directory(ies)for fingerprint data')
    parser.add_argument('-u', '--uri', required=True,
                        help='URI for database upload')
    parser.add_argument('-d', '--database', required=True,
                        help='Database name for upload')
    parser.add_argument('-c', '--collection', required=True,
                        help='Collection name for database')
    parser.add_argument('-o', '--output', required=True, help="Filename for output log")
    args = parser.parse_args()
    run(args)
