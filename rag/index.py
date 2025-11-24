from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document #Needed to wrap chunks 
from dotenv import load_dotenv
import os

load_dotenv()  
google_api_key = os.getenv("GOOGLE_API_KEY")

# Path to the PDF file
file_path = Path(__file__).parent / "mobile_computing.pdf"

# Data part of the Indexing phase
# Load this file in python program
loader = PyPDFLoader(file_path)
docs = loader.load()   #This docs is basically every single page of the pdf as a separate document

# print(docs[0]) #this will print the first page of the pdf as a document

# combine all pages into a one big string
# all_text = "".join([d.page_content for d in docs])

# Split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)

# chunks = text_splitter.split_text(all_text)

# Wrap chunks into Document objects
chunk_docs = []

for page in docs:
    page_chunks = text_splitter.split_documents([page])
    chunk_docs.extend(page_chunks)
    
# Vector embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=google_api_key,
)

# From langchain Qdrant DB
vector_store = QdrantVectorStore.from_documents(
    documents = chunk_docs,
    embedding = embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)

print("Indexing of documents is complete.")