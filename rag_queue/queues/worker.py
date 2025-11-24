from google import genai
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize GenAI client
client = genai.Client(api_key = google_api_key)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=google_api_key,
)

# Load existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    embedding = embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)

def process_query(user_query:str):
    print("Searching chunks:",user_query)
    search_results = vector_db.similarity_search(query=user_query, k=8)

    context = "\n\n".join(
        f"[Source: {result.metadata.get('source','N/A')} | Page: {result.metadata.get('page','N/A')}]\n"
        f"{result.page_content}"
        for result in search_results
    )

    SYSTEM_PROMPT = f"""
    You are a helpful AI assistant that provides accurate and concise answers to user questions based on the provided context
    along with the page_contents and page_number.
    Use only the information from the context to answer the question. 
    If the answer is not present in the context, respond with "I don't know.

    context: {context}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[
            {"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\n"
            "User Question: " + user_query}]}
            ]
    )
    return response.text
