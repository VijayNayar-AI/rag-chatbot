from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv

import os
import truststore


load_dotenv()
truststore.inject_into_ssl()


class PineconeRetriever:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )

        pinecone_db = Pinecone(
            api_key=os.getenv("PINECONE_API_KEY")
        )

        self.index = pinecone_db.Index("company-knowledge")

    def retrieve(self, query: str, top_k: int = 3):

        query_vector = self.embedding_model.embed_query(query)

        result = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )

        return result["matches"]