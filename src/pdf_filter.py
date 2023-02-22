#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import os

def pdf_filter():

    dir_main = os.path.dirname(os.path.realpath(__file__))
    dir_path = dir_main + '\output\\'
    dir_path = rf"{dir_path}"
    
    files = []

    for filename in os.listdir(dir_path):
        if filename == "gitkeep.txt":
            continue
        f = os.path.join(dir_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            files.append(f)
    
    print("Number of files before filtering: " + str(len(files)))

    keyword_excl = ["nezavezuj", "NEZAVEZUJ", "Nezavezuj"]
    keyword_incl = ["nepremi", "NEPREMI","Nepremi"]
    delete_file = None

    for file in files:
        if file[-3:] != "pdf":
            continue
        pdf_file = open(file, 'rb') 
        #-----------------------------------------
        pdf_temp = PyPDF2.PdfFileReader(pdf_file, strict=False)
        num_pages = pdf_temp.getNumPages()

        delete_file = True

        for i in range(0, num_pages):
            page = pdf_temp.getPage(i)
            text = page.extractText()
            
            for kw in keyword_incl:
                if kw in text:
                    delete_file = False
                    break

            for kw in keyword_excl:
                if kw in text:
                    delete_file = True
                    break

        #-----------------------------------------
        pdf_file.close()
        
        if delete_file:
            print(f"Deleting file: {file}.")
            os.remove(file)
    print("PDF filtering complete.")

if __name__ == "__main__":
    pdf_filter()