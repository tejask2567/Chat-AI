from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from dotenv import load_dotenv
load_dotenv()
import os
loader = DirectoryLoader('uploads/', glob="**/*.pdf", show_progress=True, loader_cls=PyPDFLoader)
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents) 
embeddings = OpenAIEmbeddings()

CONNECTION_STRING = "postgresql+psycopg2://postgres:root@localhost:5432/VECTOR_DB"

""" CONNECTION_STRING = PGVector.connection_string_from_db_params(
     driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
     host=os.environ.get("PGVECTOR_HOST", "localhost"),
     port=int(os.environ.get("PGVECTOR_PORT", "5432")),
     database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
     user=os.environ.get("PGVECTOR_USER", "postgres"),
     password=os.environ.get("PGVECTOR_PASSWORD", "root"),
 ) """

COLLECTION_NAME = "llmware"
def ingest():
    db = PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
    )
    return "Document Inegsted"

""" query = "What is viksit bharath"
docs_with_score = db.similarity_search_with_score(query) """