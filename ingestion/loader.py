from langchain_community.document_loaders import PyPDFLoader


PDF_PATH = "data/Transformers_Complete_Guide.pdf"


loader = PyPDFLoader(PDF_PATH)

documents = loader.load()

print("Total pages:", len(documents))

for document in documents[:2]:
    print("\nPage:", document.metadata.get("page"))
    print("Text:", document.page_content[:500])