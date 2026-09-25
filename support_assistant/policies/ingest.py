from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Folder containing the policy documents
POLICY_DIR = Path(__file__).parent / "policies"

# Where the vector database will be saved
DB_DIR = Path(__file__).parent / "chroma_db"


def ingest_documents():
    print("Loading policy documents...")

    loader = DirectoryLoader(
        str(POLICY_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents = loader.load()

    if not documents:
        raise ValueError(
            "No Markdown files found. Check the policies folder."
        )

    print(f"Loaded {len(documents)} policy documents.")

    # Split documents into smaller searchable chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    # Free, locally running embedding model
    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create and persist the Chroma vector database
    print("Creating Chroma vector database...")

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_DIR),
        collection_name="zepto_policies",
    )

    print(f"Database saved at: {DB_DIR}")
    print("Ingestion completed successfully!")


if __name__ == "__main__":
    ingest_documents()
