# pdf-splicer
A Python utility script to create new PDF files from pages in other PDF files.    

Use this script to create one or more PDF files that are compiled from single 
pages of other PDF files.  A table of contents file contains the mapping of pages 
in the source PDF files to pages in destination PDF files.    

Multiple destination PDFs can be created from multiple source PDFs in the same 
table of contents file.  This script processes the mappings in the table of 
contents file and produces the resulting PDFs.    

This has been useful for issuing page formatted reports that are compilations of 
PDF output from different sources.  You might have PDFs that you collect from 
others, along with visualizations from R scripts, Python scripts, 
or Power BI exports.  This script allows you to compile a single PDF digest from 
those separate documents using a template that can be rerun as often as needed.    

## Command Line     
```    
usage: pdf_splicer.py [-h] toc src_folder dest_folder    
positional arguments:    
    toc             Required: Table of contents file    
    src_folder      Required: Folder with source PDF files        
    dest_folder     Required: Folder for destination PDF files    
```    

## Table of Contents File    
The table of contents file instructs the script as to how many destination PDFs 
will result from running the script, and where to source each page of the 
destination PDFs. 

It has six columns:
1. **Report**: (Required) The name of the destination PDF file
2. **Page**: (Required) The page number in the destination PDF file
3. **Bookmark**: (Optional) The bookmark for this page
4. **Source File**: (Required) The name of the source PDF file for this page
5. **Source Page**: (Required) The page number in the source PDF file to use
6. **Folder**: (Optional) A sub-folder in the output folder to write to 

Each row in the table of contents file is intended to be a new page in a 
destination PDF file.  Multiple destination PDF files can be mapped in one 
table of contents file.    

Any table of contents record missing a value in the **Report**, **Source File**, 
or **Source Page** columns will be skipped.  Any records missing a value in 
the **Page** column will use the default page number zero.  

Technically, the script produces pages in the same 
order as the values in the **Page** column, not necessarily at the exact page 
number given in the table of contents file.  Having more than one page with 
the same destination page number will not stop the script from 
working.  The ordering of pages that share the same page number is not 
specified.    

When sequential pages share the same bookmark, the bookmark will only be applied 
to the first page in the sequence.    

## Example    
An example table of contents file, [referrals_example_toc](https://github.com/907sjl/pdf-splicer/blob/main/referrals_example_toc.csv), 
can be found in the repository.  This example uses input PDFs from my sample 
referrals report in [referrals_powerbi](https://github.com/907sjl/referrals_powerbi).    

The input for this example is a single PDF of referral process measures 
for multiple clinics.  This one PDF will be split into a report for each of those 
clinics.  Another PDF with cover sheet pages for each clinic is spliced into each 
of the destination PDFs for each clinic.    

This example also recreates the input PDF while adding bookmarks for each clinic. 
The bookmarks make it much easier for viewers to use the report.  The bookmark 
names and pages are supplied in the table of contents file.    

The shell command to run this example is:
```    
python pdf_splicer.py referrals_example_toc.csv in out 
```    
