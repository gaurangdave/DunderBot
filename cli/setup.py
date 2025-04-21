from utils.common import load_state, is_environment_ready, is_data_present, save_state
from utils.chromadb import drop_collection,create_collection
from utils.config import get_default_collection
from utils.data import convert_data_to_documents
from utils.langchain import embed_and_store_documents

def run_setup():
    ## step 0: check if required environment variables are present
    if(not is_environment_ready()):
        print("ERROR: Environment not ready")
    ## step 1: check if required data files are present
    if (not is_data_present()):
        print("ERROR: data not present!!")
    ## step 2: reset & drop the database 
    default_collection = get_default_collection()
    drop_collection(default_collection)
    ## step 3: create new collection
    create_collection(default_collection)
    ## step 4: prepare dataset
    documents = convert_data_to_documents()
    ## step 5: Upload the dataset to chromadb
    vector_db = embed_and_store_documents(documents,llm="openai")
    ## Step 6: Update the state
    save_state("is_setup_complete",True)

def reset_app():
    ## Step 1: Drop
    run_setup()

def initialize():
    ## Step 1: Load current state
    current_state,_ = load_state()
    
    ## Step 2: Check if the app is already initialized
    is_setup_complete = current_state["is_setup_complete"]
    if is_setup_complete:
        print(f"Setup is completed. Please use the run command to run the app.")
    else:
        run_setup()
    