import os
from pathlib import Path
import json
from dotenv import load_dotenv

# Load environment variables from the .env file (if present)
load_dotenv()

def get_root_directory():
    current_directory = os.getcwd()
    return current_directory


def get_data_path():
    root_dir = get_root_directory()
    data_file = Path(root_dir, "data","raw", "data.csv")
    return data_file
    

""" 
Helper function to load the state from .state.json
"""


def load_state():
    try:
        state_json = {
            "is_setup_complete": False,
            "last_updated": "",
            "model_used": ""
        }
        root_dir = get_root_directory()
        state_json_file_path = Path(root_dir, ".state.json")
        if (os.path.exists(state_json_file_path)):
            with open(state_json_file_path, "r") as state_file:
                state_json = json.load(state_file)
        else:
            with open(state_json_file_path, "w") as state_file:
                json.dump(state_json, state_file)
    except json.JSONDecodeError as err:
        print("An error occured reading the state!!", err)
    else:
        return state_json


def save_state():
    pass


# def load_env():
#     config = dotenv_values(".env")
#     return config

# Helper function to check if the environment variables are set


def is_environment_ready():
    ## TODO: This is a hacky implementation, will not work if we expand to other LLMs
    required_env_vars = ["OPENAI_API_KEY","GEMINI_API_KEY"]
    is_ready = True
    ## check for required keys
    # for env_vars in required_env_vars:
    #     if(not get_environment_vars(env_vars)):
    #         is_ready = False
    is_ready = any([get_environment_vars(env_var) for env_var in required_env_vars])
    return is_ready


def is_data_present():
    data_file = get_data_path()
    return os.path.exists(data_file)


def get_environment_vars(key):
    return os.getenv(key)
    