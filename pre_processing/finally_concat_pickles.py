import os
import pandas as pd
from pathlib import Path


PATH = "/home/user/IdeaProjects/libonea/demos/SCD/ICSI_Dataset/"

paths = sorted(Path(PATH + "Pickles/Concat/").iterdir(), key=os.path.getmtime)

initial_df = pd.read_pickle(PATH + "Pickles/Concat/" + paths[0].name)

for i in range(1, len(paths)):
    curr_pkl = pd.read_pickle(PATH + "Pickles/Concat/" + paths[i].name)
    initial_df = pd.concat([initial_df, curr_pkl])

pd.to_pickle(initial_df, PATH + "Pickles/raw_data_2_convert_2_embeddings.pkl")

pass
