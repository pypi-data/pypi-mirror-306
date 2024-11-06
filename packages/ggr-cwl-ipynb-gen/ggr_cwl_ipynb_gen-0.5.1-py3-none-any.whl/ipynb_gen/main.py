#!/usr/bin/env python

import inspect
import os
import sys
import jinja2
import nbformat
import nbformat.v3 as nbf
import numpy as np
import pandas as pd
import ruamel.yaml
from jinja2 import FileSystemLoader, PackageLoader
from jinja2.exceptions import TemplateNotFound
from xlrd import XLRDError

from . import consts

EXEC_DIR = os.path.dirname(str(__file__))


def render(tpl_path, context):
    _path, filename = os.path.split(tpl_path)
    try:
        jinja_rendered = jinja2.Environment(
            loader=FileSystemLoader(os.path.join(EXEC_DIR, "templates"))
        ).get_template(filename).render(context)
    except TemplateNotFound:
        jinja_rendered = jinja2.Environment(
            loader=PackageLoader(consts.PACKAGE_NAME, "templates")
        ).get_template(filename).render(context)
    return jinja_rendered


class Cell:
    def __init__(self, contents, description=None):
        self.contents = contents
        self.description = description
        if not isinstance(self.description, list):
            self.description = [self.description]
        self.header = []
        # self.header_inputs = []
        # self.header_outputs = []

    def writefile_to(self, dest):
        self.header = ["%%%%writefile %s" % dest]

    def to_list(self):
        cells = []
        if self.description:
            cells.append(nbf.new_text_cell('markdown', source= "\n".join(self.description)))
        if self.contents:
            cells.append(nbf.new_code_cell(input= "\n".join(self.header + self.contents)))
        return cells


class CellSbatch(Cell):
    def __init__(self, script_output=None, depends_on=False, mem=None,
                 cpus=None, partition=None, wrap_command=None, array=None,
                 prologue=None, **kwargs):
        super().__init__(**kwargs)

        if prologue is None:
            prologue = []

        content_prologue = ['sbatch']
        if script_output:
            content_prologue.extend(['-o', script_output, '\\\n'])
        if partition:
            content_prologue.extend(['-p', partition, '\\\n'])
        if mem:
            content_prologue.extend(['--mem', str(mem), '\\\n'])
        if cpus:
            content_prologue.extend(['-c', str(cpus), '\\\n'])
        if depends_on:
            content_prologue.extend(['--depend', 'afterok:$1', '\\\n'])
        if array is not None:
            content_prologue.extend(['--array', array, '\\\n'])
        if wrap_command:
            content_prologue.append('--wrap="%s' % wrap_command)
            self.contents.append('"')
        self.contents = content_prologue + self.contents
        self.contents = prologue + [' '.join(self.contents)]

        self.header = ["%%script"]
        self.header.append('--out blocking_job_str')
        self.header.append("bash")

        if depends_on:
            self.header.append('-s "$blocking_job"')
        self.header = [' '.join(self.header)]

    def to_list(self):
        cells = super().to_list()

        # We need to add an extra code cell to compute the SLURM job id
        extra_cell = Cell(
            contents=["import re",
                      r"blocking_job = re.match('Submitted batch job (\d+).*', blocking_job_str).group(1)"],
            description="Extract blocking job id"
        )
        cells.extend(extra_cell.to_list())
        return cells


def save_metadata(samples_df, conf_args, lib_type):
    cells = []
    cell_mkdir = Cell(contents=["%%bash",
                                "mkdir -p %s/data/%s/metadata" % (conf_args['root_dir'], lib_type),
                                "mkdir -p %s/data/%s/raw_reads" % (conf_args['root_dir'], lib_type),
                                "mkdir -p %s/data/%s/processed_raw_reads" % (conf_args['root_dir'], lib_type),
                                "mkdir -p %s/processing/%s/scripts" % (conf_args['root_dir'], lib_type),
                                "mkdir -p %s/processing/%s/jsons" % (conf_args['root_dir'], lib_type),
                                "mkdir -p %s/processing/%s/logs" % (conf_args['root_dir'], lib_type)
                                ],
                      description=["# %s - %s" % (conf_args['project_name'], lib_type),
                                   consts.NOTEBOOK_BLURB,
                                   "#### Create necessary folder(s)"])
    cells.extend(cell_mkdir.to_list())

    outfile = "%s/data/%s/metadata/%s_download_metadata.%s.txt" % \
              (conf_args['root_dir'], lib_type, lib_type,
               conf_args['project_name'])
    contents = ["%%%%writefile %s" %
                outfile, samples_df.to_csv(index=False,
                                           sep=conf_args['sep'],
                                           encoding='utf-8',
                                           header=[x.capitalize() for x in samples_df.columns.values])]
    cell = Cell(contents=contents, description="Save metadata file")
    cells.extend(cell.to_list())

    return cells, outfile


def download_fastq_files(conf_args, lib_type, metadata_fn=None):
    cells = []

    download_fn = "%s/processing/%s/scripts/download_%s.sh" % (conf_args['root_dir'], lib_type,
                                                               conf_args['project_name'])
    context = {
        'output_fn': download_fn,
        'project_name': conf_args['project_name'],
        'metadata_filename': metadata_fn,
        'root_dir': conf_args['root_dir'],
        'user': conf_args['user'],
        'lib_type': lib_type,
        'data_source': conf_args['data_from'],
        'consts': consts
    }
    contents = [render('templates/download_fastq_files.j2', context)]

    cell_write_dw_file = Cell(contents=contents,
                              description=["#### Download FASTQ from %s" % conf_args['data_from'],
                                           "Create file to download FASTQ files"])
    cells.extend(cell_write_dw_file.to_list())

    logs_dir = "%s/processing/%s/logs" % (conf_args['root_dir'], lib_type)
    execute_cell = CellSbatch(contents=list(),
                              partition=",".join(consts.SLURM_PARTITIONS),
                              wrap_command="ssh %s@%s 'sh %s'" % (conf_args['user'],
                                                                  consts.HOST_FOR_TUNNELED_DOWNLOAD,
                                                                  download_fn),
                              description="Execute file to download files",
                              script_output="%s/%s_%s.out" % (logs_dir, conf_args['project_name'],
                                                              inspect.stack()[0][3]))
    cells.extend(execute_cell.to_list())

    return cells


def ungzip_fastq_files(conf_args, lib_type, metadata_filename=None, num_samples=None):
    cells = []
    ungzip_fn = "%s/processing/%s/scripts/ungzip_%s.sh" % (conf_args['root_dir'], lib_type, conf_args['project_name'])
    context = {
        'output_fn': ungzip_fn,
        'metadata_filename': metadata_filename,
        'project_name': conf_args['project_name'],
        'root_dir': conf_args['root_dir'],
        'lib_type': lib_type,
        'num_samples': num_samples
    }
    contents = [render('templates/ungzip_fastq_files.j2', context)]

    cell_write_dw_file = Cell(contents=contents, description="#### Ungzip FASTQ files")
    cells.extend(cell_write_dw_file.to_list())

    logs_dir = "%s/processing/%s/logs" % (conf_args['root_dir'], lib_type)
    execute_cell = CellSbatch(contents=[ungzip_fn],
                              description="Execute file to ungzip FASTQ files",
                              depends_on=True,
                              partition=",".join(consts.SLURM_PARTITIONS),
                              array="0-%d%%20" % (num_samples - 1),
                              script_output="%s/%s_%s_%%a.out" % (logs_dir, conf_args['project_name'],
                                                                  inspect.stack()[0][3]))
    cells.extend(execute_cell.to_list())

    return cells


def merge_fastq_files(conf_args, lib_type, metadata_filename=None, num_samples=None):
    cells = []
    merge_fn = "%s/processing/%s/scripts/merge_lanes_%s.sh" % (
        conf_args['root_dir'], lib_type, conf_args['project_name']
    )
    context = {
        'output_fn': merge_fn,
        'metadata_filename': metadata_filename,
        'project_name': conf_args['project_name'],
        'root_dir': conf_args['root_dir'],
        'lib_type': lib_type,
        'num_samples': num_samples
    }
    contents = [render('templates/merge_lanes_fastq.j2', context)]

    cell_write_dw_file = Cell(contents=contents, description="#### Merge lanes of FASTQ files")
    cells.extend(cell_write_dw_file.to_list())

    logs_dir = "%s/processing/%s/logs" % (conf_args['root_dir'], lib_type)
    execute_cell = CellSbatch(contents=[merge_fn],
                              description="Execute file to merge lanes of FASTQ files",
                              depends_on=True,
                              array="0-%d%%20" % (num_samples - 1),
                              partition=",".join(consts.SLURM_PARTITIONS),
                              script_output="%s/%s_%s_%%a.out" % (logs_dir, conf_args['project_name'],
                                                                  inspect.stack()[0][3]), )
    cells.extend(execute_cell.to_list())

    return cells


def cwl_json_gen(conf_args, lib_type, metadata_filename):
    func_name = inspect.stack()[0][3]
    cells = []
    output_fn = "%s/processing/%s/scripts/%s_%s.sh" % (conf_args['root_dir'],
                                                       lib_type,
                                                       func_name,
                                                       conf_args['project_name'])
    context = {
        'output_fn': output_fn,
        'metadata_filename': metadata_filename,
        'project_name': conf_args['project_name'],
        'root_dir': conf_args['root_dir'],
        'lib_type': lib_type,
        'star_genome': consts.STAR_GENOME,
        'mem': consts.MEM[lib_type.lower()],
        'nthreads': consts.NTHREADS[lib_type.lower()],
        'separate_jsons': consts.SEPARATE_JSONS
    }
    contents = [render('templates/%s.j2' % func_name, context)]

    cell_write_dw_file = Cell(contents=contents, description="#### Create JSON files for CWL pipeline files")
    cells.extend(cell_write_dw_file.to_list())

    logs_dir = "%s/processing/%s/logs" % (conf_args['root_dir'], lib_type)
    execute_cell = CellSbatch(contents=[output_fn],
                              description="Execute file to create JSON files",
                              depends_on=True,
                              partition=",".join(consts.SLURM_PARTITIONS),
                              prologue=["source %s %s" % (consts.CONDA_ACTIVATE,
                                                          consts.CONDA_ENVIRONMENT)],
                              script_output="%s/%s_%s.out" % (logs_dir,
                                                              conf_args['project_name'],
                                                              inspect.stack()[0][3]))
    cells.extend(execute_cell.to_list())
    return cells


def cwl_slurm_array_gen(conf_args, lib_type, metadata_filename, pipeline_type, n_samples):
    func_name = inspect.stack()[0][3]
    cells = []
    output_fn = "%s/processing/%s/scripts/%s-%s.sh" % (conf_args['root_dir'],
                                                       lib_type,
                                                       conf_args['project_name'],
                                                       pipeline_type)
    metadata_basename = os.path.splitext(os.path.basename(metadata_filename))[0]
    context = {
        'output_fn': output_fn,
        'metadata_basename': metadata_basename,
        'project_name': conf_args['project_name'],
        'root_dir': conf_args['root_dir'],
        'user_duke_email': conf_args['user_duke_email'],
        'lib_type': lib_type,
        'mem': consts.MEM[lib_type.lower()],
        'nthreads': consts.NTHREADS[lib_type.lower()],
        'pipeline_type': pipeline_type,
        'consts': consts
    }
    contents = [render('templates/%s.j2' % func_name, context)]

    cell_write_dw_file = Cell(contents=contents,
                              description="#### Create SLURM array master bash file for %s samples" % pipeline_type)
    cells.extend(cell_write_dw_file.to_list())

    execute_cell = CellSbatch(contents=[output_fn],
                              description="Execute SLURM array master file",
                              depends_on=True,
                              array="0-%d%%20" % (n_samples - 1),
                              prologue=["source %s %s" % (consts.CONDA_ACTIVATE,
                                                          consts.CONDA_ENVIRONMENT)],
                              partition=",".join(consts.SLURM_PARTITIONS))
    cells.extend(execute_cell.to_list())

    return cells


def generate_qc_cell(conf_args, lib_type, pipeline_type):
    func_name = inspect.stack()[0][3]
    cells = []

    # Python program has no 'se' or 'pe' abbreviation
    end_type = pipeline_type.split("-")[0]
    if end_type == "se":
        end_type = "single_end"
    elif end_type == "pe":
        end_type = "paired_end"
    else:
        return CellSbatch(contents=[""])

    output_fn = '%s/processing/%s/scripts/%s_%s-%s.sh' % (conf_args["root_dir"],
                                                          lib_type,
                                                          func_name,
                                                          conf_args["project_name"],
                                                          pipeline_type)
    qc_type = lib_type.replace("_", "")
    context = {
        'output_fn': output_fn,
        "conda_activate": consts.CONDA_ACTIVATE,
        'root_dir': conf_args["root_dir"],
        "library_type": lib_type,
        "project_name": conf_args["project_name"],
        "pipeline_type": pipeline_type,
        "qc_script_dir": consts.QC_SCRIPT_DIR,
        "qc_type": qc_type,
        "end_type": end_type
    }
    contents = [render('templates/%s.j2' % func_name, context)]

    cell_write_dw_file = Cell(contents=contents, description="#### Create QC generating script")
    cells.extend(cell_write_dw_file.to_list())

    execute_cell = CellSbatch(contents=[output_fn],
                              depends_on=True,
                              partition=",".join(consts.SLURM_PARTITIONS),
                              description="Generate QCs for %s-%s" % (conf_args["project_name"], pipeline_type))

    cells.extend(execute_cell.to_list())

    return cells


def generate_plots(conf_args, metadata_file, lib_type, pipeline_type, n_samples):
    """
    Generates cell for creating fingerprint data
    :param conf_args: Dictionary containing data about directories, project name, etc.
    :param metadata_file: File path to metadata
    :param lib_type: Type of assay (RNA, ChIP, ATAC)
    :param pipeline_type: Type of sequencing pipeline (end, control)
    :return:
    """
    func_name = inspect.stack()[0][3]
    cells = []
    # Current iteration of web-application only accepts ChIP samples
    if lib_type != "chip_seq":
        return []

    input_directory = "{}/processing/{}/{}-{}".format(conf_args['root_dir'],
                                                      lib_type,
                                                      conf_args['project_name'],
                                                      pipeline_type)
    output_directory = input_directory

    output_fn = '%s/processing/%s/scripts/generate_plot.%s-%s.sh' % (conf_args["root_dir"],
                                                                     lib_type,
                                                                     conf_args["project_name"],
                                                                     pipeline_type)

    context = {
        'output_fn': output_fn,
        'env_activate': consts.CONDA_ACTIVATE,
        'root_dir': conf_args['root_dir'],
        'lib_type': lib_type,
        'project_name': conf_args['project_name'],
        'pipeline_type': pipeline_type,
        'metadata_file': metadata_file,
        'input_dir': input_directory,
        'output_dir': output_directory
    }
    contents = [render('templates/%s.j2' % func_name, context)]
    cell_write_dw_file = Cell(contents=contents, description="#### Create plot generating script")
    cells.extend(cell_write_dw_file.to_list())

    execute_cell = CellSbatch(contents=[output_fn],
                              depends_on=True,
                              array="0-%d%%5" % (n_samples - 1),
                              prologue=["source %s %s" % (consts.CONDA_ACTIVATE, consts.CONDA_ENVIRONMENT)],
                              partition=",".join(consts.SLURM_PARTITIONS),
                              description="Generate plots and data for website")
    cells.extend(execute_cell.to_list())

    return cells


def data_upload(conf_args, lib_type, pipeline_type):
    """
    Function for generating a cell that uploads notebook generated data
    to database. Can be avoided with usage of tag "-n".
    """
    func_name = inspect.stack()[0][3]
    cells = []

    # Only upload data to web-app if it is ChIP-seq
    if lib_type != "chip_seq" or not conf_args["upload"]:
        return []

    output_fn = '%s/processing/%s/scripts/%s_%s-%s.sh' % (conf_args["root_dir"],
                                                          lib_type,
                                                          func_name,
                                                          conf_args["project_name"],
                                                          pipeline_type)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = "{}/processing/chip_seq/{}-{}".format(conf_args['root_dir'],
                                                     conf_args['project_name'], pipeline_type)

    context = {
        'output_fn': output_fn,
        'root_dir': conf_args['root_dir'],
        'pipeline_type': pipeline_type,
        'library_type': lib_type,
        'project_name': conf_args['project_name'],
        'script_dir': consts.DATA_UPLOAD_SCRIPT,
        'conda_activate': consts.CONDA_ACTIVATE,
        'data_dir': data_dir,
        'uri': conf_args['uri'] if 'uri' in conf_args else None,
        'database': conf_args['database'] if 'database' in conf_args else None,
        'collection': conf_args['collection'] if 'collection' in conf_args else None
    }

    contents = [render('templates/%s.j2' % func_name, context)]
    cell_write_dw_file = Cell(contents=contents, description="#### Create data upload script")
    cells.extend(cell_write_dw_file.to_list())

    execute_cell = CellSbatch(contents=[output_fn],
                              depends_on=True,
                              prologue=["source %s alex" % consts.CONDA_ACTIVATE],
                              partition=",".join(consts.SLURM_PARTITIONS),
                              description="### Upload ChIP-seq to web-application")
    cells.extend(execute_cell.to_list())

    return cells


def get_pipeline_types(samples_df):
    lib_type = samples_df['library type'].iloc[0].lower().replace('-', '_')
    if lib_type == consts.LIBRARY_TYPE_CHIP_SEQ:
        for seq_end in consts.SEQ_ENDS:
            for with_control in consts.WITH_CONTROLS:
                samples_filter = samples_df['paired-end or single-end'].str.lower() == seq_end
                if with_control:
                    samples_filter = samples_filter & (~samples_df['control'].isnull())
                    pipeline_type = '-'.join([seq_end, with_control])
                else:
                    samples_filter = samples_filter & (samples_df['control'].isnull())
                    pipeline_type = '-'.join([seq_end])
                yield pipeline_type, np.sum(samples_filter)
    if lib_type == consts.LIBRARY_TYPE_RNA_SEQ:
        for seq_end in consts.SEQ_ENDS:
            for strandness in consts.STRANDNESSES:
                samples_filter = \
                    (samples_df['paired-end or single-end'].str.lower() == seq_end) \
                    & (samples_df['strand specificity'].str.lower() == strandness)
                if consts.WITH_SJDB:
                    pipeline_type = '-'.join([seq_end, strandness, 'with-sjdb'])
                else:
                    pipeline_type = '-'.join([seq_end, strandness])
                yield pipeline_type, np.sum(samples_filter)
    if lib_type == consts.LIBRARY_TYPE_ATAC_SEQ:
        for seq_end in consts.SEQ_ENDS:
            for with_blacklist_removal in consts.BLACKLIST_REMOVAL:
                samples_filter = (samples_df['paired-end or single-end'].str.lower() == seq_end)
                if with_blacklist_removal:
                    pipeline_type = '-'.join([seq_end, with_blacklist_removal])
                    samples_filter = samples_filter & (~samples_df['blacklist removal'].isnull())
                else:
                    pipeline_type = '-'.join([seq_end])
                    samples_filter = samples_filter & (samples_df['blacklist removal'].isnull())
                yield pipeline_type, np.sum(samples_filter)
    if lib_type == consts.LIBRARY_TYPE_STARR_SEQ:
        for seq_end in consts.SEQ_ENDS:
            for with_umis in consts.WITH_UMIS:
                samples_filter = (samples_df['paired-end or single-end'].str.lower() == seq_end)
                if with_umis:
                    pipeline_type = '-'.join([seq_end, with_umis])
                    if 'umis' in samples_df.columns:
                        samples_filter = samples_filter & samples_df['umis']
                else:
                    pipeline_type = '-'.join([seq_end])
                    if 'umis' in samples_df.columns:
                        samples_filter = samples_filter & ~samples_df['umis']
                yield pipeline_type, np.sum(samples_filter)


def data_acquisition_cells(conf_args, lib_type, metadata_file, nsamples):
    cells = []
    if conf_args['data_from'] != consts.DATA_SOURCES_LOCAL:
        cells.extend(download_fastq_files(conf_args,
                                          lib_type,
                                          metadata_fn=metadata_file))
        cells.extend(merge_fastq_files(conf_args,
                                       lib_type,
                                       metadata_filename=metadata_file,
                                       num_samples=nsamples))
    else:
        download_fn = "%s/data/%s/processed_raw_reads/%s" % (
            conf_args['root_dir'], lib_type,
            conf_args['project_name'])
        warning_cell = Cell(contents=None,
                            description=["### FASTQ files already available locally!!",
                                         "Please, make sure the FASTQ files are correctly named, decompressed and located/symlinked in:",
                                         "", "**", download_fn, "**"])
        cells.extend(warning_cell.to_list())

    return cells


def create_cells(samples_df, conf_args=None):
    """
    Master function to write all code and text for the notebook.

    Conceptually, there are a number of things that have to happen:
        - save metadata txt file
        - download FASTQ.gz files from sequencing core
        - uncompress FASTQ.gz files
        - rename and move FASTQ files
        - create JSONs files for cwltool
        - execute cwltool master file
    """
    lib_type = samples_df.iloc[0]['library type'].lower().replace('-', '_')
    num_samples = samples_df.shape[0]
    cells = []

    cc, metadata_file = save_metadata(samples_df, conf_args, lib_type)
    cells.extend(cc)

    cells.extend(data_acquisition_cells(conf_args, lib_type, metadata_file, num_samples))
    cells.extend(cwl_json_gen(conf_args, lib_type, metadata_filename=metadata_file))
    for pipeline_type, n in get_pipeline_types(samples_df):
        if n > 0:
            cells.extend(cwl_slurm_array_gen(conf_args, lib_type, metadata_filename=metadata_file,
                                             pipeline_type=pipeline_type, n_samples=n))
            cells.extend(generate_qc_cell(conf_args, lib_type, pipeline_type=pipeline_type))
            cells.extend(generate_plots(conf_args, metadata_file=metadata_file,
                                        lib_type=lib_type, pipeline_type=pipeline_type, n_samples=n))
            cells.extend(data_upload(conf_args, lib_type, pipeline_type))

    return cells


def make_notebook(outfile, metadata, conf_args=None):
    """Create notebook with parsed contents from metadata"""
    nb = nbf.new_notebook()

    cells = []
    # Create a notebook by Library type existing in the metadata file
    for samples_df in get_samples_by_library_type(metadata, conf_args['sep']):
        cells.extend(create_cells(samples_df, conf_args=conf_args))

    nb['worksheets'].append(nbf.new_worksheet(cells=cells))

    with open(outfile, 'w') as _:
        nbformat.write(nb, _)


def get_samples_by_library_type(metadata_file, sep='\t'):
    """
    Parse a metadata file (either a spreadsheet or a tab-delimited file.

    :return: generator of panda's dataframe
    """
    try:
        md = pd.read_excel(metadata_file.name,
                           true_values=['Yes', 'Y', 'yes', 'y', 1],
                           false_values=['No', 'N', 'no', 'n', 0])
    except XLRDError:
        print(XLRDError)
        md = pd.read_csv(metadata_file.name,
                         true_values=['Yes', 'Y', 'yes', 'y', 1],
                         false_values=['No', 'N', 'no', 'n', 0], sep=sep)

    md.columns = [x.lower() for x in md.columns]
    named_cols = [c for c in md.columns if not c.startswith('unnamed: ')]
    lib_types_found = set(md['library type'][~pd.isnull(md['library type'])])

    for lt in lib_types_found:
        yield md.loc[md['library type'] == lt, named_cols]


def init_conf_args(args, required_args=None, optional_args=None):
    if required_args is None:
        required_args = ['root_dir']

    if optional_args is None:
        optional_args = ['user', 'sep', 'user_duke_email', 'project_name']

    conf_args = {}
    if args['conf_file']:
        conf_args = ruamel.yaml.load(args['conf_file'], Loader=ruamel.yaml.Loader)
    for r in required_args:
        conf_args[r] = args[r] if (r in args and args[r]) else conf_args[r]
        try:
            assert conf_args[r] is not None
        except AssertionError:
            print("[ERROR]", r, "not defined")
            raise
    for o in optional_args:
        conf_args[o] = args[o] if (o in args and args[o]) else (conf_args[o] if o in conf_args else None)
    conf_args['user'] = conf_args['user'] or os.environ['USER']
    conf_args['user_duke_email'] = conf_args['user_duke_email'] or "%s@duke.edu" % conf_args['user']
    conf_args['project_name'] = conf_args['project_name'] or \
                                os.path.splitext(os.path.basename(args['metadata'].name))[0]

    return conf_args


def run(args):
    conf_args = init_conf_args(vars(args))
    outfile = "%s.ipynb" % conf_args['project_name']

    if os.path.isdir(args.out):
        outfile = os.path.join(args.out, outfile)
    else:
        outfile = args.out

    if os.path.isfile(outfile) and not args.force:
        print(outfile, "is an existing file. Please use -f or --force to overwrite the contents")
        sys.exit(1)

    conf_args['upload'] = args.no_upload
    conf_args['data_from'] = args.data_from

    make_notebook(outfile,
                  args.metadata,
                  conf_args=conf_args)
