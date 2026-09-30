from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = "data/Transformers_Complete_Guide.pdf"

#load pdf 
loader = PyPDFLoader(PDF_PATH)
documents=loader.load()

print("Total pages :", len(documents))

#create text splitter 
text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks=text_splitter.split_documents(documents)
print("Total chunks :", len(chunks))

# 4. Display first 3 chunks
for i, chunk in enumerate(chunks[:3]):

    print("\n" + "=" * 60)
    print("Chunk:", i + 1)
    print("Page:", chunk.metadata.get("page"))
    print("Text:")
    print(chunk.page_content)