'''
Filename            : 3_view.py
Path                : util 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : PDF Viewer of FOI    
Copyright           : All rights Reserved to KIKU 
'''

import base64 
import os 
import yaml

from raga.util import session, log, config
from raga.util.html import htmlPages as html
from raga.util.process.rag_10_summarize import summarize_file
from raga.util.process.rag_11_classify import classify_file
from util.db import sql_docs as docs

pdf_tab, json_tab, graph_tab, info_tab = html.tabs(["PDF", "JSON", "GRAPH", "INFO"])

def view_graph(graph) :
    with graph_tab : 
        html.show_message(graph)

def view_json(doc_id, json=None) :
    with json_tab : 
        if json is None :
            pass
            
            # template_list = docs.get_template_list()
            # selected_template = html.get_selectbox("Select Template", template_list)
            # if html.get_button("Classify"):
            #     templatpython e_details = docs.get_template_details(selected_template)
            #     template_yaml = yaml.safe_load(template_details)
            #     json = classify_file(pdf_file_path, template_yaml)
            #     docs.sql_update_json(doc_id, json)
            
        else :
            html.show_message(json)

def view_info(doc_id, pdf_file_path) : 
    with info_tab : 
        doc_detail = docs.sql_get_doc_detail(doc_id)
        html.show_message("Document Name : " + doc_detail[0])
        html.show_message("Page Count: " + str(doc_detail[1]))
        html.show_message("Document Type: " + doc_detail[2])
        
        if doc_detail[3] == "" :
            if html.get_button("Get Summary") : 
                summary = summarize_file(pdf_file_path)
                html.show_message(summary)
                docs.sql_update_summary(doc_id, doc_detail[3])
        else : 
            html.show_message("Summary: " + doc_detail[3])

        

def view_pdf(pdf_path):
    
    # with open(file_path,"rb") as f:
    #     base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    # st.markdown(pdf_display, unsafe_allow_html=True)
    
    #with open(pdf_file_path, "rb") as f:
    #    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    #pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="inherit" height="1000" type="application/pdf"></iframe>'
    #pdf_display = f'<div class = "view-pdf"> <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height ="1000px" type="application/pdf"></iframe></div>'
    pdf_display = f'<div class = "view-pdf">' 
    pdf_display += f'<iframe src="{pdf_path}" width="100%" height="1000px" type="application/pdf"></iframe>'
    pdf_display += f'</div>'
    #print ("3_view: ", pdf_display)
    with pdf_tab : 
        html.show_markdown(pdf_display, unsafe_allow_html=True)


if __name__ == "__main__":     

    # with html.st_sidebar : 
    #     yaml_file = html.file_uploader("Upload the template and click on Extract", type = ["yaml"], accept_multiple_files=False)
    #     yaml_button = html.get_button("Extract")
    
    if not (logged_in := session.get_value(session.LOGGED_IN)):
        html.show_error ("Please login through the login page")
    else :
        if (pdf_file_name := session.get_value(session.PDF_FILE_NAME)) is not None: 
            pdf_file_path = os.path.join(config.HOME + "\\static\\docs",pdf_file_name)
            pdf_path = "app/static/docs/" + pdf_file_name
            doc_id = session.get_value(session.DOC_ID)
            page_num = session.get_value(session.PDF_PAGE_NUM)
            log.log_debug(f"3_view: {pdf_path=} {doc_id=} {page_num=}")
            if page_num is not None and page_num > 0 : 
                pdf_path += f"#page={page_num}" 
            #print(f"3_view: {pdf_path}")
            view_pdf(pdf_path)
            view_json(doc_id)
            view_info(doc_id, pdf_file_path)
        else : 
            html.error ("Please select a document from the cabinet")
            html.page_link("pages/2_cabinet.py", label="Cabinet")


