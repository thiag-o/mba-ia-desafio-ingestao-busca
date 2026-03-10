import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL" )
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")

def ingest_pdf():
    loader = PyPDFLoader(str(PDF_PATH))
    
    splits = loader.load_and_split(RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    ))
    if not splits:
        raise SystemExit(0)

    enrichedDocs = []
    for split in splits:
        document = Document(
            page_content=split.page_content,
            metadata={k: v for k, v in split.metadata.items() if v not in ("", None)}
        )
        enrichedDocs.append(document)   

    ids = [f"doc-{i}" for i in range(len(enrichedDocs))]

    embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)
    
    
    for e in enrichedDocs:
        print(e.metadata.items())

    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )



    store.add_documents(ids=ids,documents=enrichedDocs)



if __name__ == "__main__":
    ingest_pdf()