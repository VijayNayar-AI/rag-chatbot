from langchain_community.document_loaders import PyPDFLoader 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import truststore

truststore.inject_into_ssl()

PDF_PATH = "data/Transformers_Complete_Guide.pdf"

#load pdf 
loader = PyPDFLoader(PDF_PATH)
documents=loader.load()

#splitter the document 
text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks=text_splitter.split_documents(documents)

#load embedding model s

embedding_model= HuggingFaceEmbeddings( model="sentence-transformers/all-MiniLM-L6-v2")

#extract from every chunk 
texts=[chunk.page_content for chunk in chunks ]

#convert into vectors
vector=embedding_model.embed_documents(texts)

print("Total embeddings:", len(vector))
print("Dimension of first embedding:", len(vector[0]))