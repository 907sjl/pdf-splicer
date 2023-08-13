# pdf-splicer
A Python utility script to create new PDF files from pages in other PDF files.    

Use this script to create one or more PDF files that are compiled from single 
pages of other PDF files.  A table of contents file contains the mapping of pages 
in the source PDF files to pages in destination PDF files.    

Multiple destination PDFs can be created from multiple source PDFs in the same 
table of contents file.  This script processes the mappings in the table of 
contents file and produces the resulting PDFs.    

This has been useful for issuing page formatted reports that are compilations of 
PDF output from different sources.  You might have PDFs collected from others 
that contain data, along with visualizations from R scripts, Python scripts, 
or Power BI exports.  This script allows you to compile a single PDF digest from 
those separate documents with a template that can be rerun as often as needed.    

## Command Line     
```    
usage: pdf_splicer.py [-h] toc src_folder dest_folder    
positional arguments:    
    toc             Required: Table of contents file    
    src_folder      Required: Folder with source PDF files        
    dest_folder     Required: Folder for destination PDF files    
```    
