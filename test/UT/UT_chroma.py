from langchain.memory import ConversationBufferMemory

## sample conversation using Chroma DB 
from foi.util.models import rag_llama31
from foi.util.vector import chroma 
from foi.util.process import rag_02_embedding as embed 


def sample_conversation_test():

    test_collection = chroma.client.get_or_create_collection(name="test")
    print (f"Sample Test : {type(test_collection)}")
    doc1 = "The capital of Japan is Tokyo"
    doc2 = "Shakespeare is from Stratford upon Avon"
    doc3 = "Mary had a little lamb and the lamb was white as milk"

    input_text = "Who is the best playwright in the world?"
    #log.log_write(f"handle_userinput:: chat history(before) = {chat_history}")
    test_collection.add(ids=["ID01", "ID02", "ID03"]
                   ,documents=[doc1, doc2, doc3]
                   ,metadatas=[{"source": "Japan"}, {"source": "England"}, {"source": "India"}]
                )
    print (f"Sample Test after add: {type(test_collection)}")

    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    conversation = rag_llama31.get_conversation_chain(chroma.vectorstore) 
    response = conversation({'question': input_text})
    chat_history = response['chat_history']
    
    while not input_text.startswith("exit") :
        qe1 = chroma.embeddings([input_text])
        results = chroma.collection.query (
            query_texts=input_text,
            n_results = 1
            )
        print (results)
        system_prompt = 'Use this context :  ' + results["documents"] 
        response = conversation({'question': input_text, "prompt": system_prompt})
        chat_history = response['chat_history']
    
        input_text = input("PLease enter your next question(type exit to quit)")

def sample_conversation_docs():

    from langchain_chroma.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI

    docs_collection = chroma.client.get_or_create_collection(name="docs")
    input_text = "Which US state's captive regulations are explained?"
    #log.log_write(f"handle_userinput:: chat history(before) = {chat_history}")
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages =True) 
    vectorstore = Chroma.from_documents(documents=docs_collection, embedding=OpenAIEmbeddings())
    conversation = rag_llama31.get_conversation_chain(vectorstore) 
    response = conversation({'question': input_text})
    chat_history = response['chat_history']
    
    while not input_text.startswith("exit") :
        qe1 = chroma.embeddings([input_text])
        results = chroma.collection.query (
            query_texts=input_text,
            n_results = 1
            )
        print (results)
        system_prompt = 'Use this context :  ' + results["documents"] 
        response = conversation({'question': input_text, "prompt": system_prompt})
        chat_history = response['chat_history']
    
        input_text = input("PLease enter your next question(type exit to quit)")

def test_semantic_search():

    
    question = "Where should we submit the electronic application in New Jersey for application of Captive registration?"
    
    question_embeddings = embed.get_embeddings("Llama3.1", "chroma",[question])
    result = chroma.semantic_search (question, question_embeddings, n_results = 1)
    print (result)

if __name__ == "__main__" :
    print (f"Collections = {chroma.list_collections()}")
    test_semantic_search()
    #sample_conversation_test()
    #sample_conversation_docs()


