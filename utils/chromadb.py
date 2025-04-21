import chromadb
from chromadb.config import Settings
from utils.common import get_environment_vars, get_root_directory
from pathlib import Path
import os

from utils.config import get_default_db_path


def get_or_create_db_path():
    # helper function to create directories for db
    db_path = get_default_db_path()
    if (not os.path.exists(db_path)):
        os.makedirs(db_path)
    return str(db_path)


def get_database_client():
    db_path = get_or_create_db_path()
    client = chromadb.PersistentClient(
        path=db_path,
    )
    return client


def get_collection(collection_name):
    client = get_database_client()
    collection = client.get_or_create_collection(name=collection_name)
    return collection


def drop_collection(collection_name, llm="openai"):
    try:
        client = get_database_client()
        if collection_name in [c for c in client.list_collections()]:
            client.delete_collection(collection_name)
            return True
        else:
            print(f"INFO: No collection with the name {collection_name}")
            return False
    except ValueError as verr:
        print(f"ERROR: deleting the collection {verr}")
        return False

def create_collection(collection_name):
    client = get_database_client()
    return client.get_or_create_collection(name=collection_name)