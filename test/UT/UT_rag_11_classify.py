from datetime import datetime as dt 
import glob
import json 

import yaml
from raga.util import config as cfg 
yaml_file = cfg.HOME + cfg.path[cfg.YAML] + cfg.filename[cfg.YAML]
with open(yaml_file, 'r') as file : 
    output_format_dict = yaml.safe_load(file)
print(output_format_dict)

def test_classify (): 
    from raga.util.process.rag_11_classify import classify_file

    pdf_folder =  "C:\\Personal\\KIKU\\insuranceFoundationModel\\captives\\Regulatory\\southCarolina\\"
    of = open(pdf_folder + "JSON.txt", "w", encoding="utf-8")
        # pdf_file = "C:\\Personal\\KIKU\\insuranceFoundationModel\\captives\\Regulatory\\southCarolina\\" + \
        #             "Consent to Service of Process for Captive Insurance Companies_201409110819208357.pdf"
    for pdf_index, pdf_file in enumerate(glob.glob(pdf_folder + "Ca*.pdf")) : 
        start_time = dt.now()
        print(start_time.strftime("%d/%m/%Y %H:%M:%S %f"), f": {pdf_index} {pdf_file} ")
        s = f": {pdf_index} {pdf_file} \n"
        of.write (s)
        s = "-" * 40 + "\n"
        of.write(s) 
        method = "stuff"  ## "mapreduce"
        #json_structure = {"country" : "<USA/India/Japan/Other>", "state": "<state>", "summary" : "<summary>"}
        
        summary = classify_file(pdf_file, output_format_dict )
        
        #of.write(summary) 
        #of.write ("\n")
        #s = "*" * 40 + "\n"
        #of.write(s)
        #of.write(summary["output_text"]) 
        of.write(summary)
        of.write ("\n")
        s = "*" * 40 + "\n"
        of.write(s)        
        end_time = dt.now()
        print(end_time.strftime("%d/%m/%Y %H:%M:%S %f"), f": {pdf_index} completed in (", end_time - start_time, ") seconds")
    of.close()
    return "success" 

if __name__ == "__main__": 
    #result = test_classify()
    #print(result)

    from util.db import sql_docs as docs
    docs_df = docs.sql_get_doc_list("govindjpn@gmail.com")
    country_state_set = set(list(zip(docs_df.country, docs_df.state)))
    print (country_state_set)
