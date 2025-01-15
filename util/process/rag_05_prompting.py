
'''
Filename            : rag_05_prompting.py
Path                : util/process 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Prompting Algorithms  
Copyright           : All rights Reserved to KIKU 
'''

from langchain_core.prompts import ChatPromptTemplate

def get_prompt(retrieved_documents, chat_history, user_question): 
    #prompt = f"Use this context : {retrieved_documents}. History : {chat_history} Now answer this question : {user_question}"

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "PLease use this context to answer the question : {context} Chat History  {history}" 
        ),
        ("human", "{input}"),
    ]
    )   

    return prompt 