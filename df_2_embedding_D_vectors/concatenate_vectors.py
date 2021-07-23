import os
import pandas as pd
from pathlib import Path


PATH = "/home/user/IdeaProjects/libonea/demos/SCD/ICSI_Dataset/Pickles/"

paths = sorted(Path(PATH + "vec/").iterdir(), key=os.path.getmtime)

all_data = pd.read_pickle(PATH + "vec/" + paths[0].name)

for i in range(1, len(paths)):
    curr_pkl = pd.read_pickle(PATH + "vec/" + paths[i].name)
    all_data = pd.concat([all_data, curr_pkl], ignore_index=True)

print("Size before dropna: " + str(len(all_data)))
all_data = all_data.sample(frac=1)

all_data = all_data.dropna()
print("Size after dropna: " + str(len(all_data)))

print("Defining train size")
train_size = int(0.8 * len(all_data))

train_df = all_data.head(train_size)
print("Train Size: " + str(len(train_df)))

test_df = all_data.tail(len(all_data) - train_size)
print("Test Size: " + str(len(test_df)))

pd.to_pickle(train_df, PATH + 'ICSI-Hybrid_Data_Vectors-Speech-NLP_Train.pkl')
pd.to_pickle(test_df, PATH + 'ICSI-Hybrid_Data_Vectors-Speech-NLP_Test.pkl')

pass
