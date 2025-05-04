from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

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


def retrieve_documents(user_query, filter=None, number_of_results=10):
    try:
        vector_db = get_vector_db(llm="openai")
        results = vector_db.similarity_search(
            query=user_query, k=number_of_results, filter=filter or None)
        return results
    except RuntimeError as re:
        print(f"[Warning] Skipping retrieval due to error: {re}")
        return []


def initialize_chat_model(llm="openai"):
    # TODO: Refactor this to support more llms
    if (llm == "openai"):
        model = get_default_model()

    chat_model = init_chat_model(model=model, model_provider="openai")
    return chat_model


def format_query_optimizer_prompt(user_query):
    query_optimizer_prompt = """
        You are an intelligent query optimization agent for a Retrieval-Augmented Generation (RAG) system.
        Your job is to:
        1. Deduce the most relevant short search string (`user_query`) to use for **similarity search** in a ChromaDB vector store.
        2. Suggest how many documents to retrieve (`number_of_results`, typically between 3 and 10).
        3. Propose an optional **metadata filter** using ChromaDB’s filtering syntax to narrow the search.

        We are using **ChromaDB**, which supports metadata filters using a **Mongo-style syntax**.

        You may use these comparison operators:
        - `$eq`, `$ne`, `$gt`, `$lt`, `$ge`, `$le`
        - `$in`, `$nin` (for lists of values)
        - `$and`, `$or` (for combining multiple filters)

        You can filter using these metadata fields:
        - `season` (integer)
        - `episode` (integer)
        - `scene` (integer)
        - `speakers` (string; comma-separated names`)
        - `episode_description` (string)
        - `rating` (float)
        - `directed_by` (string)
        - `written_by` (string; comma-separated names`)

        Examples:
        - To filter by speaker and season:
        {{
            "$and": [
            {{"season": {{"$eq": 2}}}},
            {{"speakers": {{"$in": ["Dwight"]}}}}
            ]
        }}
        - To match any of two directors:
            {{
                "directed_by": {{"$in": ["Ken Kwapis", "Greg Daniels"]}}
            }}
        Output Format:
        Return your response in valid JSON format with these exact keys:
        {{
        "user_query": "...",
        "number_of_results": 5,
        "filter": {{
            ...
        }}
        }}
        Instructions:
        - If the user includes season, episode, speaker, director, etc., use them in the filter.
        - Combine multiple filters using $and.
        - If no filters are relevant, return "filter": {{}}.
        - Do NOT explain anything. Only return the final JSON output.

        User Query:
        {user_query}
    """
    prompt_template = ChatPromptTemplate.from_template(query_optimizer_prompt)
    return prompt_template.invoke({"user_query": user_query})


def format_response_prompt(user_query, context_documents):
    system_template = """
        You are DunderBot 🤖 — an assistant trained on dialogue and episode metadata from *The Office* TV show.

        {{%- if context %}}
        Use the following excerpts from the show to answer the user's question. Be witty, fun, and stay true to the characters — but do not make things up.

        ---------------------
        {context}
        ---------------------

        {{%- else %}}
        Unfortunately, I couldn't find any relevant scenes from the show to help with this question. Still, try your best to answer it briefly and in-character using your general knowledge of *The Office*.

        {{%- endif %}}
    """

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


def generate_json_response(prompt, chat_model):
    # chat_model = initialize_chat_model(llm="openai")
    parser = JsonOutputParser()
    chain = chat_model | parser
    reponse = chain.invoke(prompt)
    return reponse
