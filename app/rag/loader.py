"""
PDF Loading utility
This module extracts raw text from the AWS Customer Agreement PDF using PyMuPDF.
"""

import fitz

def load_pdf(file_path: str) -> str:
    """    
    loads a pdf and extracts all it's raw text
    """
    document = fitz.open(file_path)
    text = ""

    for page in document:
        text+= page.get_text() # for every page in document, append its text
    
    document.close()

    return text