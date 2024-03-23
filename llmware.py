from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
import os
from langchain.chains import ConversationalRetrievalChain
load_dotenv()

os.environ["OPENAI_API_KEY"] =os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings()

CONNECTION_STRING = "postgresql+psycopg2://postgres:root@localhost:5432/VECTOR_DB"
COLLECTION_NAME = "llmware"
store = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
)
retriever = store.as_retriever( search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5})
memory = ConversationBufferMemory(return_messages=True,memory_key='chat_history')
llm = ChatOpenAI()
qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, memory=memory,retriever = retriever)

def llmware(query):
    prompt=query
    if prompt=="quit":
        exit(0)
    response = qa_chain({'question':prompt,'chat_history':[]})
    return (response['answer'])
