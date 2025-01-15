from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.llms import Ollama
# Prompt
from langchain_core.prompts import PromptTemplate
# Define LLM Chain

from langchain.chains.llm import LLMChain
# Create full chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from util import log


def convert_to_prompt(format_dict): 
    def convert_field(f, v):
        pv = "" 
        if f != "version_info" : 
            if isinstance(v, dict):
                pv += f + "( "
                for f1, v1 in v.items(): 
                    pv +=  convert_field(f1, v1) 
                pv = pv[0:-1] + "),"
            else: 
                pv += f + ","
            return pv
        return "" 

    def convert_field_values(f, v):
        if f != "version_info" : 
            pv = "" 
            if isinstance(v, dict):
                for f1, v1 in v.items(): 
                    pv += convert_field_values(f1, v1)
            elif isinstance(v, list):
                pv += f"For {f}, select one value from {v} \n"
            elif isinstance(v, str):
                pv += f"For {f}, {v[1:-1]} \n"
            else: 
                pv += f"For {f}, {v} \n"
            return pv
        return "" 

    #fields = ",".join(field for field in format_dict.keys() if field != "info")
   
    fields = ""
    values = ""
    for field, field_values in format_dict.items() : 
        if field != "version_info" :
            fields += convert_field(field, field_values)
            values += convert_field_values(field, field_values)        
    return fields + "\n" + values 

llm = Ollama(model="llama3.1:latest")

def classify_file(pdf_file, format_dict): 
    loader = PyPDFLoader(pdf_file)
    document = loader.load()
    format_str = convert_to_prompt(format_dict)
    #print (format_str)
    prompt_template = """
                    Please provide the response in JSON format with the following fields : {output_format}
                        The summary should be within 50 words. 
                        Only include information that is part of the document. 
                        Do not include your own opinion or analysis. 
                        The output should be only in JSON. Any description should be wrapped within the JSON structure.
                        For example, put the summary within the field called "summary"
                    Document :
                    "{context}"
                    """
    prompt = PromptTemplate.from_template(prompt_template)
    stuff_chain = create_stuff_documents_chain(llm, prompt)

    log.log_debug(f"PDF File :: {pdf_file}\n")
    log.log_debug(f"Instruction : {format_str}\n")

    result = stuff_chain.invoke({"context": document, "output_format": format_str})
    #result = format_str
    
    log.log_debug(result)

    return result 

