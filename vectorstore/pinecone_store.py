from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from pinecone import Pinecone
from dotenv import load_dotenv

import os
import truststore


# Load environment variables
load_dotenv()

truststore.inject_into_ssl()


PDF_PATH = "data/Transformers_Complete_Guide.pdf"


# 1. Load PDF
loader = PyPDFLoader(PDF_PATH)

documents = loader.load()

print("Total pages:", len(documents))


# 2. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Total chunks:", len(chunks))


# 3. Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2"
)


# 4. Extract chunk text
texts = [chunk.page_content for chunk in chunks]


# 5. Create embeddings
vectors = embedding_model.embed_documents(texts)

print("Total embeddings:", len(vectors))
print("Dimension:", len(vectors[0]))


# 6. Connect to Pinecone
pinecone_db = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)


# 7. Connect to existing index
index = pinecone_db.Index("company-knowledge")


# 8. Create Pinecone records
records = []

for i, chunk in enumerate(chunks):

    record = {
        "id": f"transformer-{i + 1}",

        "values": vectors[i],

        "metadata": {
            "text": chunk.page_content,
            "source": chunk.metadata.get("source"),
            "page": chunk.metadata.get("page", 0)
        }
    }

    records.append(record)


# 9. Upload records to Pinecone
index.upsert(vectors=records)


print("All documents stored successfully!")