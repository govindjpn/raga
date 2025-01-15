'''
Filename            : rag_07_conversation.py
Path                : util/process 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Controller of FOI    
Copyright           : All rights Reserved to KIKU 
'''
#from langchain.memory import ConversationBufferMemory

from raga.util import log, session 
#from raga.util.models import rag_llama31 #vrag_openai   # , rag_huggingface, rag_gemma, 
from raga.util.process import rag_01_chunking as chunk 
from raga.util.process import rag_02_embedding as embed 
from raga.util.process import rag_03_semantic_search as search 
from raga.util.process import rag_04_reranking as rerank 
from raga.util.process import rag_05_prompting as prompt 
from raga.util.process import rag_06_consolidation as consol 

from raga.util.models import rag_llama31 as l31 
from raga.util.models import rag_openai as oai 

from raga.util.vector import vectordb as vdb 



''' Conversation Chain 
def get_conversation_chain(chat_model, vectorstore) :
    log.log_write(f"get_conversation_chain :: Model = {chat_model}")
    #memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    match chat_model : 
        case "OpenAI": 
            conversation_chain = rag_openai.get_conversation_chain(vectorstore) 
        #case "HuggingFace" : 
        #    conversation_chain = rag_huggingface.get_conversation_chain(vectorstore) 
        #case "Gemma" :
        #    conversation_chain = rag_gemma.get_conversation_chain(vectorstore) 
        case "Llama3.1" : 
            conversation_chain = None # rag_llama31.get_conversation_chain(vectorstore)
        case _ :   
            conversation_chain = rag_openai.get_conversation_chain(vectorstore)    
    log.log_write(f"get_conversation_chain :: conversation_chain = {type(conversation_chain)}")
    return conversation_chain


'''




def answer_question (user_question) : 

    embedding_model = session.get_value(session.EMBEDDING_MODEL)
    chat_model = session.get_value(session.CHAT_MODEL)
    vectordb= session.get_value(session.VECTORDB)
    conversation_chain =  session.get_value(session.CONVERSATION)
    chat_history = session.get_value(session.CHAT_HISTORY)
    rag_flag = session.get_value(session.RAG_FLAG)
    chat_history_str = ""

    
    if chat_history is not None : 
        for i, message in enumerate(chat_history): 
            if i%2 == 0 : 
                chat_history_str.join(f"Question : {message}\n")
            else :
                chat_history_str.join(f"Answer: {message}\n")

    if rag_flag : 
        ## Change the question to Embedding 
        question_embeddings = embed.get_embeddings(embedding_model, vectordb,[user_question])
        print (f"Question Embeddings :: {type(question_embeddings)}:: {user_question}")


        ## Perform a semantic Search of the question against the database 
        semantic_results = search.get_search_result(vectordb, user_question, question_embeddings)
        print (f"Semantic Results :: {type(semantic_results)}:: {str(semantic_results)}")

        retrieved_docs = semantic_results["documents"]
        retrieved_ids = semantic_results["ids"]
        if retrieved_docs[0] is None or len(retrieved_docs[0]) == 0:
            print(f"No match found in semantic search")
            retrieved_docs = ""
            reranked_responses = ""
            reranked_ids = [[]]
            chat_history_str = ""
            question_prompt = prompt.get_prompt(None, None, user_question)
        else : 
            ## rerank the responses 
            reranked_responses, reranked_ids = rerank.get_reranking(retrieved_docs, retrieved_ids)
            print (f"Reranked Response :: {type(reranked_responses)}:: {reranked_responses[0]}")
            print (f"Reranked IDs :: {type(reranked_ids)}:: {reranked_ids[0]}")

            ## generate the prompt 
            question_prompt = prompt.get_prompt(reranked_responses, chat_history, user_question)
            print (f"Prompt :: *** {type(question_prompt)}:: {question_prompt}")
    else :
        retrieved_docs = ""
        reranked_responses = ""
        chat_history_str = ""
        question_prompt = prompt.get_prompt(None, None, user_question)

    
    ##  invoke the LLM 
    match chat_model : 
        case "OpenAI": 
            # vector_store = vdb.get_vectorstore(chat_model, "chroma")
            # conversation_chain = oai.get_conversation_chain(vector_store)
            # llm_response = conversation_chain({"question": question_prompt, "history": chat_history_str, "chat_history": chat_history_str})
            # responses = [llm_response]
            chain = question_prompt | oai.llm
            response = chain.invoke(
                {
                "context": reranked_responses,
                "history": chat_history_str,
                "input": user_question,
                }
                )   
            print (f"Response(after invoke) :: ====  {type(response)}::{type(response.content)} ")
            print (f"Response(after invoke) :: ====  RAG = {rag_flag} :: {str(response.content)}")
            # 
            if not isinstance(response.content, str):
                print (f"Respo(nses :: ====  {type(response)}::{type(response.content)} :: {str(response.content)}")
                response = response.content
            response_str = response.content
            if rag_flag and len(reranked_ids[0]) > 0: 
                response_str = response_str + "(###" + reranked_ids[0][0] + "###)" 
            responses = [response_str]
            print (f"Responses(Modified, OpenAI) :: ====  {type(responses)}:: {str(responses)}")



        case "Llama3.1" :
            
            chain = question_prompt | l31.llm
            response = chain.invoke(
                {
                "context": retrieved_docs,
                "history": chat_history_str,
                "input": user_question,
                }
                )   
            print (f"Response(after invoke) :: ====  {type(response)}::{type(response.content)} ")
            print (f"Response(after invoke) :: ====  RAG = {rag_flag} :: {str(response.content)}")
            # 
            if not isinstance(response.content, str):
                print (f"Responses :: ====  {type(response)}::{type(response.content)} :: {str(response.content)}")
                response = response.content
            response_str = response.content
            if rag_flag:
                response_str = response_str + "(###" + reranked_ids[0][0] + "###)" 
            responses = [response_str]
            print (f"Responses(Modified, Llama 3.1) :: ====  {type(responses)}:: {str(responses)}")

            
        case _ :
            chain = question_prompt | oai.llm
            response = chain.invoke(
                {
                "context": retrieved_docs,
                "history": chat_history_str,
                "input": user_question,
                }
                )   
            responses = [response]
            print (f"Responses :: ====  {type(responses)}:: {str(responses)}")
            # 
            if not isinstance(response.content, str):
                print (f"Responses :: ====  {type(response)}::{type(response.content)} :: {str(response.content)}")
                response = response.content
            response_str = response.content
            if rag_flag:
                response_str = response_str + "(###" + reranked_ids[0][0] + "###)" 
            responses = [response_str]
            print (f"Responses(Modified, Llama 3.1) :: ====  {type(responses)}:: {str(responses)}")

    ## consolidate the response 
    consolidated_response = consol.get_consolidation(responses)

    log.log_debug(f"answer_question : <= {type(consolidated_response)}  {str(consolidated_response)}")
    return consolidated_response 


