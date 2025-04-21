import os
import json
from pathlib import Path
from utils.common import get_root_directory

def get_configuration(key):
    root_dir = get_root_directory()
    config_file_path = Path(root_dir, "config.json")
    if(os.path.exists(config_file_path)):
        with open(config_file_path,"r") as configuration:
            config_json = json.load(configuration)
            return config_json[key]

def get_default_db_path():
    return get_configuration("default_db_path")

def get_default_collection():
    return get_configuration("default_collection")

def get_default_model():
    return get_configuration("default_model")