from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings

from utils.chromadb import get_or_create_db_path


def create_document_chunks(documents):
    # Step 1: create array of LangChain Document
    docs = [
        Document(page_content=doc["text"], metadata=doc["metadata"])
        for doc in documents
    ]
    # Step 2: Create chunks from langchain docs
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,  # Estimated based on avg words per scene
        chunk_overlap=50  # Ensures context continuity
    )

    # Apply text splitter to break large chunks into smaller ones
    split_docs = text_splitter.split_documents(docs)

    # Step 3:Create document IDs based on chunks
    split_doc_ids = []
    for i, doc in enumerate(split_docs):
        base_id = doc.metadata["id"]
        chunk_id = f"{base_id}_chunk{i}"  # make sure each chunk is unique
        split_doc_ids.append(chunk_id)
    return split_docs, split_doc_ids


def embed_and_store_documents(documents, llm="openai"):
    # Step 1: initialize embedding function
    # TODO: Refactor this to support more llms
    if (llm == "openai"):
        embedding_function = OpenAIEmbeddings()

    # Step 2: Create document chunks
    split_docs, split_doc_ids = create_document_chunks(documents=documents)

    # Step 3: Update chroma db with the embeddings
    persistant_directory = get_or_create_db_path()
    vector_db = Chroma.from_documents(
        split_docs, embedding_function, ids=split_doc_ids, persist_directory=persistant_directory)
    collection_count = vector_db._collection.count()
    
    print(f"Successfully loaded {collection_count} docs to the DB")
    return vector_db
