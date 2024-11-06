#!/usr/bin/env python3
import argparse
from ipynb_gen.main import run
import ipynb_gen.consts as consts

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Generator of Jupyter notebooks to execute CWL pre-processing pipelines')
    parser.add_argument('-o', '--out', required=True, type=str, help='Jupyter notebook output file name')
    parser.add_argument('-m', '--metadata', required=True, type=argparse.FileType('r'),
                        help='Metadata file with samples information')
    parser.add_argument('-f', '--force', action='store_true', help='Force to overwrite output file')
    parser.add_argument('-n', '--no-upload', action='store_false',
                        help='Avoids uploading generated data to database when specified')
    parser.add_argument('--metadata-sep', dest='sep', required=False, type=str, default='\t',
                        help='Separator for metadata file (when different than Excel spread sheet)')
    parser.add_argument('--project-name', required=False, type=str,
                        help='Project name (by default, basename of metadata file name)')
    parser.add_argument('--data-from', required=False, choices=consts.data_sources,
                        default=consts.data_sources[0],
                        help='Choices: %s' % (', '.join(consts.data_sources)))
    parser.add_argument('-c', '--conf-file', required=False, type=argparse.FileType('r'),
                        help='YAML configuration file (see examples)')
    parser.add_argument('-u', '--user', required=False,
                        help='HARDAC User used in SLURM (default: ${USER})')
    parser.add_argument('-e', '--user-duke-email', required=False,
                        help='Email(s) notified when execution is finished (default: ${USER}@duke.edu)')
    parser.add_argument('-r', '--root-dir', required=False,
                        help='Root directory where all subfolders and files will be created '
                             '(semi-required: either defined here or in conf-file)')
    parser.add_argument('-v', '--version', required=False,
                        help='Print version of the program and exit')

    args = parser.parse_args()
    run(args)

