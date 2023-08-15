"""
pdf_splicer.py
A script to create one or more PDF files from individual pages of multiple PDF files.
https://907sjl.github.io/
"""

import os
import argparse
import pathlib as pl
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

HELP_DESCRIPTION = 'Create one or more PDF files that are compiled from single pages of other PDF files.  ' \
                   + 'A table of contents file contains the mapping of pages in the source PDF files ' \
                   + 'to pages in destination PDF files.'

TOC_COLUMNS = {
    'Report': 'string'
    , 'Page': 'float'
    , 'Bookmark': 'string'
    , 'Source File': 'string'
    , 'Source Page': 'float'
    , 'Folder': 'string'
}


def get_report_name(row) -> str:
    """
    Returns the sub-folder and report name path combination associated with the given
    table of contents mapping row.  This will be the relative path to the report when
    it is saved to storage.
    :param row: The page mapping row
    :return: The relative path to the report when saved to storage
    """
    if pd.isnull(row['Folder']):
        report_path = (row['Report']).replace(' ', '_') + r'.pdf'
    else:
        report_path = os.path.join(row['Folder'], (row['Report']).replace(' ', '_') + r'.pdf')
    return report_path


def write_pdf(report_name, writer):
    """
    Writes a PDF file to storage.
    :param report_name: The relative file path to the stored PDF
    :param writer: The PyPDF2 PDFWriter object to stream into the file
    :return: None
    """
    out_path = os.path.join(parameters['dest_folder'], report_name)

    # Make directories if needed
    head, tail = os.path.split(out_path)
    if (head):
        pl.Path(head).mkdir(parents=True, exist_ok=True)

    # Write file into directory
    with open(out_path, "wb") as fp:
        writer.write(fp)


def load_toc(toc_path) -> pd.DataFrame:
    """
    Loads the mapping data of source pages to destination reports.
    :param toc_path: The file path for the mappings
    :return: A dataframe with the mappings
    """
    print('Loading', toc_path, 'as table of contents')
    toc_df = pd.read_csv(toc_path, dtype=TOC_COLUMNS)
    toc_df['Page'] = toc_df['Page'].fillna(0).astype('int64')
    toc_df['Source Page'] = toc_df['Source Page'].fillna(-1).astype('int64')
    toc_df.sort_values(by=['Report', 'Folder', 'Page'], ascending=[True, True, True], inplace=True)
    toc_df.reset_index(drop=True, inplace=True)
    return toc_df


def load_source_pdfs(in_folder_path, toc) -> dict[str, PdfReader]:
    """
    Loads the source PDF pages.
    :param in_folder_path: The folder with the source PDF files
    :param toc: The dataframe with the page mappings
    :return: A dictionary of source file names to PDFReader objects
    """
    source_data = {}
    source_files = toc['Source File'].unique()
    for source_file in source_files:
        if pd.isnull(source_file):
            continue
        source_file_path = list(pl.Path(in_folder_path).glob(source_file+'.pdf'))[0]
        print('Loading', source_file_path, 'as source pdf')
        reader = PdfReader(source_file_path)  # open input
        n = len(reader.pages)
        print(n, 'pages')
        source_data.update({source_file: reader})
    return source_data


def parse_command_line_parameters() -> dict[str, str]:
    """
    Collects the command line parameters into a dictionary.
    :return: A dictionary of parameter names and values
    """
    parser = argparse.ArgumentParser(
        description=HELP_DESCRIPTION
        , formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('toc', help='Required: Table of contents file')
    parser.add_argument('src_folder', help='Required: Folder with source PDF files')
    parser.add_argument('dest_folder', help='Required: Folder for destination PDF files')
    args = parser.parse_args()
    config = vars(args)
    return config


"""
MAIN
"""
parameters = parse_command_line_parameters()

# Load page mapping data and source PDF files
toc_df = load_toc(parameters['toc'])
sources = load_source_pdfs(parameters['src_folder'], toc_df)

# Open an output stream for the first destination PDF
# and initialize variables
writer = PdfWriter()
new_pdf_page = 0
report_name = 'none'
last_bookmark = 'none'

# Loop over the mapping data records of source pages to destination PDFs
if (len(toc_df.index) > 0):
    for index, row in toc_df.iterrows():
        print(row['Folder'], row['Report'], row['Bookmark'], row['Source Page'])
        if (pd.isnull(row['Report']) or pd.isnull(row['Source File']) or (row['Source Page']==-1)):
            continue

        # If the destination in this record is different from the last
        # record then write the previous file and open a new output stream
        this_report_name = get_report_name(row)
        if ((this_report_name != report_name) and (report_name != 'none')):
            write_pdf(report_name, writer)
            writer = PdfWriter()
            new_pdf_page = 0
        report_name = this_report_name

        # Add the page from the source PDF to the output stream
        this_source = row['Source File']
        source_page = row['Source Page']
        reader = sources[this_source]
        writer.add_page(reader.pages[source_page - 1])

        # If the bookmark changed from the previous record then add
        # a new bookmark to the destination PDF at this page
        if pd.isnull(row['Bookmark']):
            this_bookmark = ''
        else:
            this_bookmark = row['Bookmark']
        if ((this_bookmark != last_bookmark) and (this_bookmark)):
            writer.add_outline_item(this_bookmark, new_pdf_page, parent=None)
        last_bookmark = this_bookmark

        new_pdf_page += 1
        # END of mapping record loop

    # After all mapping records processed, if there were any then
    # make sure to write the last output stream to a PDF file
    if (report_name != 'none'):
        write_pdf(report_name, writer)
