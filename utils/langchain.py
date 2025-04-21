from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from utils.chromadb import get_or_create_db_path
from utils.config import get_default_model


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


def get_vector_db(llm="openai"):
    # Step 1: initialize embedding function
    # TODO: Refactor this to support more llms
    if (llm == "openai"):
        embedding_function = OpenAIEmbeddings()

    # Step 2: initialize vectordb instance
    persistant_directory = get_or_create_db_path()
    vector_db = Chroma(persist_directory=persistant_directory,
                       embedding_function=embedding_function)
    return vector_db


def retrieve_documents(user_query, number_of_results=10):
    vector_db = get_vector_db(llm="openai")
    results = vector_db.similarity_search(
        query=user_query, k=number_of_results)
    return results


def initialize_chat_model(llm="openai"):
    # TODO: Refactor this to support more llms
    if (llm == "openai"):
        model = get_default_model()

    chat_model = init_chat_model(model=model, model_provider="openai")
    return chat_model


def format_prompt(user_query, context_documents):
    system_template = """
    You are DunderBot 🤖 trained on quotes from The Office TV show.
    Use the following episode content to answer the user's question. Be fun, but don't make things up.
    ---------------------
    {context}
    ---------------------"""

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_template), ("user", "{user_query}")
    ])
    context = "\n\n".join(
        [f"Lines : {doc.page_content}\nInfo : {doc.metadata}" for doc in context_documents])
    return prompt_template.invoke({
        "context": context,
        "user_query": user_query
    })

def generate_response(prompt, chat_model):
    # chat_model = initialize_chat_model(llm="openai")
    reponse = chat_model.invoke(prompt)
    return reponse.content