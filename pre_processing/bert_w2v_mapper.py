import pandas as pd
from bert_embedding import BertEmbedding


PATH = "/home/user/IdeaProjects/libonea/demos/SCD/ICSI_Dataset/"

df = pd.read_pickle(PATH + "Pickles/general_df_4_all_files.pkl")
words = sorted(list(set(list(df["Word"]))))

words_dictionary = {}

bert_embedding = BertEmbedding()

index = 0
for word in words:
    result = bert_embedding([word])
    words_dictionary.update({word: result[0][1][0]})
    index += 1
    print(index)

pd.to_pickle(words_dictionary, PATH + "Models/Word2Vec/bert_w2v_dictionary.pkl")

pass
