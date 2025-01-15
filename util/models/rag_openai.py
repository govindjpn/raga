'''
Filename            : rag_openai.py
Path                : util/process 
Author              : KIKUGO 
Created             : Oct 2024
Purpose             : Interface to OpenAI
Copyright           : All rights Reserved to KIKU 
'''

from langchain_community.embeddings import OpenAIEmbeddings 
from langchain_community.chat_models import ChatOpenAI  
#from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import util.log as log 


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
)

def get_conversation_chain(vectorstore) :
    """
    Return a conversation chain that uses the given vectorstore to retrieve
    documents and the OpenAI chat model to generate responses.

    :param vectorstore: The vectorstore to use for retrieval
    :return: A ConversationalRetrievalChain
    """
    log.log_write(f"get_conversation_chain -> ")
    #memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    llm = ChatOpenAI()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        #memory=memory
        )
    log.log_write(f"get_conversation_chain :: conversation_chain = {type(conversation_chain)}")
    return conversation_chain


def main() : 
    pass

if __name__ == "__main__" :
    main()
