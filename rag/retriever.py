import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DOC_PATH = "rag/docs"
BASE_DB_PATH = "rag/vectorstores"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

def build_vector_store(category: str):
    """
    Builds a specific vector store for a given category (e.g., 'returns', 'shipping').
    """
    source_path = os.path.join(BASE_DOC_PATH, category)
    db_path = os.path.join(BASE_DB_PATH, category)

    if not os.path.exists(source_path):
        print(f"⚠️ Folder {source_path} not found. Skipping.")
        return None

    # Load PDFs from the specific category folder
    loader = DirectoryLoader(source_path, glob="*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()

    if not docs:
        print(f"⚠️ No documents found in {category}.")
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # Create and Save local FAISS index
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(db_path)
    print(f"✅ Built index for '{category}' at {db_path}")
    return db

def get_retriever(category: str):
    """
    Loads the specific vector store for the requested category.
    """
    db_path = os.path.join(BASE_DB_PATH, category)
    
    # Check if DB exists; if not, try to build it
    if not os.path.exists(db_path):
        db = build_vector_store(category)
        if not db:
            return None
    else:
        db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    
    return db.as_retriever(search_kwargs={'k': 3})

# Initialize all DBs when running this script directly
if __name__ == "__main__":
    for cat in ["returns", "shipping", "general","cancel"]:
        build_vector_store(cat)