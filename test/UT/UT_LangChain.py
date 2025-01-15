
'''
https://python.langchain.com/v0.1/docs/use_cases/question_answering/chat_history/
'''

from langchain.chains import create_history_aware_retriever
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_chroma import Chroma
from dotenv import load_dotenv
import bs4

load_dotenv() # To get OPENAI_API_KEY

def create_vectorstore_retriever():
    """
    Returns a vector store retriever based on the text of a specific web page.
    """
    URL = r'https://lilianweng.github.io/posts/2023-06-23-agent/'
    loader = WebBaseLoader(
        web_paths=(URL,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(class_=("post-content", "post-title", "post-header"))
        ))
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0, add_start_index=True)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    return vectorstore.as_retriever()


def create_prompt():
    """
    Returns a prompt instructed to produce a rephrased question based on the user's
    last question, but referencing previous messages (chat history).
    """
    system_instruction = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instruction),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")])
    return prompt


llm = ChatOpenAI(model='gpt-4o-mini')
vectorstore_retriever = create_vectorstore_retriever()
prompt = create_prompt()

history_aware_retriever = create_history_aware_retriever(
    llm,
    vectorstore_retriever,
    prompt
)

chat_history = []

docs = history_aware_retriever.invoke({'input': 'what is planning?', 'chat_history': chat_history})
for i, doc in enumerate(docs):
    print(f'Chunk {i+1}:')
    print(doc.page_content)
    print()


chat_history = [
    ('human', 'when I ask about planning I want to know about Task Decomposition too.')]

docs = history_aware_retriever.invoke({'input': 'what is planning?', 'chat_history': chat_history})
for i, doc in enumerate(docs):
    print(f'Chunk {i+1}:')
    print(doc.page_content)
    print()