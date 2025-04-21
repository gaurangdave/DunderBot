from utils.common import load_state, is_environment_ready, is_data_present
from utils.chromadb import drop_collection,create_collection
from utils.config import get_default_collection

def run_setup():
    ## step 0: check if required environment variables are present
    if(not is_environment_ready()):
        print("Environment not ready")
    ## step 1: check if required data files are present
    if (not is_data_present()):
        print("data not present!!")
    ## step 2: reset & drop the database 
    default_collection = get_default_collection()
    drop_collection(default_collection)
    ## step 3: create new collection
    create_collection(default_collection)

def initialize():
    ## Step 1: Load current state
    current_state = load_state()
    
    ## Step 2: Check if the app is already initialized
    is_setup_complete = current_state["is_setup_complete"]
    if is_setup_complete:
        print(f"Setup is completed. Please use the run command to run the app.")
    else:
        run_setup()
    