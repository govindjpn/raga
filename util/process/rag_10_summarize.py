from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.llms import Ollama
# Prompt
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
# Create full chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from foi.util import log



llm = Ollama(model="llama3.1:latest")

def summarize_file(pdf_file): 
    loader = PyPDFLoader(pdf_file)
    document = loader.load()

    prompt_template = """Write a short summary of the following document not exceeding 100 words. 
                        Only include information that is part of the document. 
                        Do not include your own opinion or analysis.    
                    Document:   
                    "{context}"
                    Summary:
                    """
    prompt = PromptTemplate.from_template(prompt_template)
    llm_chain = prompt  | llm
    #stuff_chain = create_stuff_documents_chain(llm_chain, prompt)    
    result = llm_chain.invoke({"context":document})
    return result
