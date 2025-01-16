import os
from PyPDF2 import PdfReader

from util import log, session, doc_definition as doc


def get_pdf_text(pdf_file, store_pdf = True) -> dict: 
    pdf_reader = PdfReader(pdf_file)
    text = {}
    for index, page in enumerate(pdf_reader.pages) :
        text[index + 1] = page.extract_text()
    #log.log_write(text)
    log.log_write(f"get_pdf_text:: {pdf_file} #pages = {len(pdf_reader.pages)}")

    if store_pdf : 
        # save a copy in docs folder 
        with open(os.path.join("static\\docs",pdf_file.name),"wb") as f: 
            f.write(pdf_file.getbuffer())
            
        # add an entry in the docs table 
        doc_info = doc.Document(doc_id=0)
        doc_info.user_id = session.get_value(session.USER_ID)
        doc_info.doc_name = pdf_file.name 
        doc_info.doc_pathname = os.path.join("static\\docs",pdf_file.name)
        doc_info.doc_password = "" ## LATER 
        doc_info.doc_type = "PDF"
        doc_info.doc_page_count = len(PdfReader(pdf_file).pages)
        doc_info.doc_summary = ""

    return text, doc_info 
