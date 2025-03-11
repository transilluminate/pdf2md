#!/usr/bin/env python3

import re
from pathlib import Path
from dotenv import dotenv_values

# this uses IBM Docling for conversion: https://ds4sd.github.io/docling/
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TesseractCliOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption, WordFormatOption, SimplePipeline

# this backend seems to get better results
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

def main():

    # load the environment from the .env file, see .env.example
    config = dotenv_values(".env")

    # you can override the environment using this (for testing)
    config = {
        #"PATH_TO_CONVERT": "./testpdfs",
        "PATH_TO_CONVERT": "~/Zotero/storage/YXYPZ997",
        "FORCE_REINDEX": "True",
    }

    # variable names for ease of reading
    path_to_convert = config["PATH_TO_CONVERT"]
    force_reindex   = config["FORCE_REINDEX"]

    # deal with '~' if supplied and resolve symlinks etc.
    path_to_convert = Path(path_to_convert).expanduser().resolve()

    # define extensions that the converter can use
    extensions = ['.pdf', '.docx', '.doc', '.pptx', '.html', '.htm']

    # recursively glob for all valid files within that path
    file_list = list(filter(lambda path: path.suffix in extensions, Path(path_to_convert).rglob('*')))

    # total number of files to convert
    n = len(file_list)
    print(f"Found {n} valid files in {path_to_convert} ...")
    
    # integer to store the file numbder for a progress monitor
    i = 1

    for file_path in file_list:

        # we create a accompanying file with a .md extension (input.pdf.md)
        # this will make it easier in to append the extension to the existing
        # pdf links with the citations plugin: ![[{{entry.files.[0].md}}]]
        md_path = Path(f"{file_path}.md")

        # filename wrangling for displaying progress
        file_name = Path(file_path).name
        md_name = Path(md_path).name

        # this can take a while, so have a progres monitor
        percent_complete = (i / n) * 100
        
        # display progress
        print(f"{i}/{n} ({percent_complete:.1f}%) Checking: {file_name}")
        
        # increment now so when we 'continue' later, we don't forget!
        i += 1 

        if (force_reindex == "True" or not Path.exists(md_path)):

            print(" -> Extracting document text ...")

            # Configure pipeline options
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = False  # Disable OCR temporarily
            pipeline_options.do_table_structure = True

            # Create converter
            converter = DocumentConverter(
                allowed_formats=[
                    InputFormat.PDF,
                    InputFormat.DOCX,
                    InputFormat.HTML,
                    InputFormat.PPTX,
                ],
                format_options={
                    InputFormat.PDF: PdfFormatOption(
                        pipeline_options=pipeline_options,
                        backend=PyPdfiumDocumentBackend
                    ),
                    InputFormat.DOCX: WordFormatOption(
                        pipeline_cls=SimplePipeline
                    )
                }
            )

            result = converter.convert(file_path)
            if not result or not result.document:
                raise ValueError(f" -> Failed to convert document: {file_name}")

            print(" -> Starting conversion to Markdown ...")
            markdown = result.document.export_to_markdown()

            print(f" -> Cleaning Markdown ...")
            markdown = re.sub('(<!--.*?-->)', '', markdown, flags=re.DOTALL)    # remove comments
            markdown = re.sub("(w?) ' s","'s", markdown, flags=re.DOTALL)       # silly quotes
            markdown = re.sub('&amp;','&', markdown)                            # ampersands
            markdown = re.sub(r"\[(.+?)\]",r'\1', markdown)                     # brackets
            markdown = re.sub("\n+","\n",markdown)                              # multiple line breaks

            print(f" -> Writing file: {md_name}")
            with open(md_path, "w", encoding="utf-8") as handle:
                handle.write(markdown)

        else: # md file already exists and we aren't forcing a re-index
                        
            print(f" -> Markdown already exists: {md_name}")
            continue # skip the file

if __name__ == "__main__":
    main()