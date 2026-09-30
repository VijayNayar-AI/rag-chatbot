from langchain_groq import ChatGroq
from dotenv import load_dotenv

from retrieval.retriever import PineconeRetriever
from prompts.rag_prompt import rag_prompt

import os
import truststore


load_dotenv()
truststore.inject_into_ssl()


class RAGChain:

    def __init__(self):

        # Load LLM
        self.llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0
        )

        # Load retriever
        self.retriever = PineconeRetriever()

    def ask(self, question: str):

        # 1. Retrieve relevant documents
        matches = self.retriever.retrieve(
            question,
            top_k=3
        )

        # 2. Extract text from retrieved documents
        context = "\n\n".join(
            match["metadata"]["text"]
            for match in matches
        )

        # 3. Create prompt
        prompt = rag_prompt.invoke({
            "context": context,
            "question": question
        })

        # 4. Send prompt to LLM
        response = self.llm.invoke(prompt)

        return response.content