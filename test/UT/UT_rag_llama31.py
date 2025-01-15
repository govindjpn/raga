from datetime import datetime as dt 
import glob


'''
def test_summarize (): 
    from raga.util.process.rag_11_classify import summarize_file

    pdf_folder =  "C:\\Personal\\KIKU\\insuranceFoundationModel\\captives\\Regulatory\\southCarolina\\"
    of = open(pdf_folder + "summary.txt", "w", encoding="utf-8")
        # pdf_file = "C:\\Personal\\KIKU\\insuranceFoundationModel\\captives\\Regulatory\\southCarolina\\" + \
        #             "Consent to Service of Process for Captive Insurance Companies_201409110819208357.pdf"
    for pdf_index, pdf_file in enumerate(glob.glob(pdf_folder + "A*.pdf")) : 
        start_time = dt.now()
        print(start_time.strftime("%d/%m/%Y %H:%M:%S %f"), f": {pdf_index} {pdf_file} ")
        s = f": {pdf_index} {pdf_file} \n"
        of.write (s)
        s = "-" * 40 + "\n"
        of.write(s) 
        method = "stuff"  ## "mapreduce"
        summary = summarize_file(pdf_file, method)
        
        #of.write(summary) 
        #of.write ("\n")
        #s = "*" * 40 + "\n"
        #of.write(s)
        of.write(summary["output_text"]) 
        of.write ("\n")
        s = "*" * 40 + "\n"
        of.write(s)
        print (summary["output_text"])
        of.write("\n")
        
        end_time = dt.now()
        print(end_time.strftime("%d/%m/%Y %H:%M:%S %f"), f": {pdf_index} completed in (", end_time - start_time, ") seconds")
    of.close()

    '''


def test_classify (): 
    from raga.util.process.rag_11_classify import classify_file

    pdf_folder =  "C:\\Personal\\KIKU\\insuranceFoundationModel\\captives\\Regulatory\\southCarolina\\"
    of = open(pdf_folder + "JSON.txt", "w", encoding="utf-8")
        # pdf_file = "C:\\Personal\\KIKU\\insuranceFoundationModel\\captives\\Regulatory\\southCarolina\\" + \
        #             "Consent to Service of Process for Captive Insurance Companies_201409110819208357.pdf"
    for pdf_index, pdf_file in enumerate(glob.glob(pdf_folder + "A*.pdf")) : 
        start_time = dt.now()
        print(start_time.strftime("%d/%m/%Y %H:%M:%S %f"), f": {pdf_index} {pdf_file} ")
        s = f": {pdf_index} {pdf_file} \n"
        of.write (s)
        s = "-" * 40 + "\n"
        of.write(s) 
        method = "stuff"  ## "mapreduce"
        summary = classify_file(pdf_file, method)
        
        #of.write(summary) 
        #of.write ("\n")
        #s = "*" * 40 + "\n"
        #of.write(s)
        of.write(summary["output_text"]) 
        of.write ("\n")
        s = "*" * 40 + "\n"
        of.write(s)        
        end_time = dt.now()
        print(end_time.strftime("%d/%m/%Y %H:%M:%S %f"), f": {pdf_index} completed in (", end_time - start_time, ") seconds")
    of.close()
    return "success" 


def test_ollama_client ():
    from ollama import Client
    client = Client(host='http://localhost:11434')
    print ("Client Initialized")
    response = client.chat(model='llama3.1', messages=[
        {
        'role': 'user',
        'content': 'Why is the sky blue?',
        },
    ])
    return response

def test_ollama_chat ():
    
    import ollama
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model="llama3.1",
        temperature=0,
        # other params...
    )
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "PLease use this context to answer the question : {context}",
        ),
        ("human", "{input}"),
    ]
    )   
    document = "Valluvar is the best known Tamil Poet"
    chain = prompt | llm
    response = chain.invoke(
    {
        "context": document ,
        "input": "Who is the best known Tamil Poet?",
    }
    )   
    
    # response = ollama.chat(model='llama3.1', messages=[
    #     {
    #     'role': 'system'
    #     'conte'
    #     'role': 'user',
    #     'content': 'Why is the sky blue?',
    #     },
    # ])
    # print(response['message']['content'])
    return response


def test_ollama_chain (): 
    from langchain.chat_models.ollama import ChatOllama
    from langchain.chains import ConversationChain
    from langchain.memory import ConversationBufferMemory
    
    ## Memory example
    llm = ChatOllama(temperature=0.0, model='llama3.1:latest')
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)
    ## First round
    resoponse = chain("Hello, can you say just say hi?")
    print (response)
    ## Second round 
    response = chain("what about a goodbye")
    print (response)

    return 


def test_ollama_history(): 
    
    from ollama import Ollama
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_community.chat_models import ChatOpenAI
    from langchain.chains import create_history_aware_retriever
    from langchain import hub

    llm_model ="llama3.1"
    llm = Ollama(model=llm_model)
    contextualize_q_system_prompt = (
        "Given the chat history and the latest user question, "
        "provide a response that directly addresses the user's query based on the provided  documents. "
        "Do not rephrase the question or ask follow-up questions."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    #history_aware_retriever = create_history_aware_retriever(
    #    llm, retriever, contextualize_q_prompt
    #)
    system_prompt = (
        "As a personal chat assistant, provide accurate and relevant information based on the provided document in 2-3 sentences. "
        "Answe should be limited to 50 words and 2-3 sentences.  do not prompt to select answers or do not formualate a stand alone question. do not ask questions in the response. "
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    #rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    ### Statefully manage chat history ###
    store = {}
    # def get_session_history(session_id: str) -> BaseChatMessageHistory:
    #     if session_id not in store:
    #         store[session_id] = ChatMessageHistory()
    #     return store[session_id]
    conversational_rag_chain = None     
    #      RunnableWithMessageHistory(
    #     rag_chain,
    #     get_session_history,
    #     input_messages_key="input",
    #     history_messages_key="chat_history",
    #     output_messages_key="answer",
    # )
    print("Conversational chain created")
    return conversational_rag_chain


if __name__ == "__main__": 
    #test_summarize()
    #result = test_ollama_client()
    #result = test_ollama_chain()
    #result = test_ollama_chat()
    result = test_classify()
    print(result)

