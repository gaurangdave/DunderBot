from pathlib import Path
import pandas as pd
import numpy as np

from utils.common import get_root_directory


def load_data():
    root_dir = get_root_directory()
    data_dir = Path(root_dir, "data", "raw")
    data = pd.read_csv(Path(data_dir,"data.csv"))
    return data

def convert_data_to_documents():
    data = load_data()
    ## step 1: sort data by season, episode and id
    data = data.sort_values(by=["season","episode","id"])
    
    ## step 2: group data by season and episode
    grouped_data = data.groupby(["season","episode"])
    
    ## step 3: loop thru grouped data and convert it into list of documents
    # initializing list of documents
    documents = []
    # loop thru the grouped data to create documents and metadata
    for (season, episode), group in grouped_data:
        '''
            Here season, episode is of type numpy.int64 and group is a pandas.DataFrame
        '''
        # read total scenes from this episode
        total_scenes = group["total_scenes"].iloc[0]

        # break group into scene chunks
        scene_chunks = np.array_split(group, total_scenes)

        # loop thru each scene to create document, and metadata
        for i, chunk in enumerate(scene_chunks):
            scene_number = i + 1  # start with scene number 1
            unique_id = f"s{season}_e{episode}_scene{scene_number}"
            # Step 3.1: Combine lines from pseudo episode
            # TODO Does it make sense in adding new line character after each line? I don't think so, but something to confirm later.
            combined_lines = " ".join(chunk["lines"].values)

            # Step 3.2: Create an array of speakers in this scene
            # most of the times the speakers are repeated, since a pseudoscene might be between 2 people
            speaker_list = list(
                map(lambda speaker: speaker.strip(), chunk["speaker"].unique().tolist()))

            # Step 3.3: Retrive episode description
            episode_description = chunk["description"].iloc[0]

            # Step 3.4: Add episode start/end markers if needed
            if i == 0:
                combined_lines = f"--- Episode Start ---\n{episode_description}\n{combined_lines}"
            elif i == len(scene_chunks) - 1:
                combined_lines = f"{combined_lines}\n--- Episode End ---"

            # Step 3.5: Create metadata object        
            ## we are converting lists to string, cause ChromaDB metadat doesn't support list
            ## will need to look into other solution for better querying
            
            written_by = ",".join(list(map(lambda writer: writer.strip(), chunk["written_by"].iloc[0].split("|"))))
            
            metadata = {
                "id":unique_id,
                "season": int(season), ## converting to int cause metadata only supports int
                "episode": int(episode),
                "scene": int(scene_number),
                "speakers": ",".join(speaker_list),
                "episode_description": episode_description,
                "rating": float(chunk["rating"].iloc[0]),
                "directed_by": chunk["directed_by"].iloc[0].strip(),
                "written_by": written_by
            }

            # Step 3.6: Append document to the document list
            documents.append({
                "text": combined_lines,
                "metadata": metadata
            })
    return documents