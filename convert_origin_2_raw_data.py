import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


PATH = "/home/user/IdeaProjects/libonea/demos/SCD/ICSI_Dataset/"


class WordObject:
    def __init__(self, fn, w, start, end, speaker):
        self.file_name = fn
        self.word = w
        self.start_time = start
        self.end_time = end
        self.speaker = speaker


os.chdir(PATH + "Data/ICSI_plus_NXT/Words")
all_file_name = glob.glob("*.xml")
all_file_name.sort(key=lambda x: os.path.getmtime(x))

files = [x.split(".")[0] for x in all_file_name]
files = sorted(list(set(list(files))))

files_set = {}
for key in files:
    files_set.update({key: []})

err_count = 0

for f_name in all_file_name:

    file_words = []

    tree = ET.parse(PATH + "Data/ICSI_plus_NXT/Words/" + f_name)
    root = tree.getroot()

    file_id = f_name.split(".")[0]
    file_speaker = f_name.split(".")[1]

    if len(file_speaker) > 0:  # because of the file Buw001..words that has no speaker
        for child in root:
            tag = child.tag
            attribute = child.attrib

            if 'w' == tag:
                if attribute['c'] == 'W':
                    word = child.text

                    try:
                        start_time = float(attribute['starttime'])
                        end_time = float(attribute['endtime'])
                    except:
                        continue

                        # err_count += 1
                        # if "" == attribute['starttime']:
                            # start_time = float(attribute['endtime']) - 0.3
                        # if "" == attribute['endtime']:
                            # end_time = float(attribute['starttime']) + 0.3

                    word_to_add = WordObject(file_id, word, start_time, end_time, file_speaker)
                    file_words.append(word_to_add)

        files_set[file_id].append(file_words)

pd.to_pickle(files_set, PATH + "Pickles/files_df.pkl")

pass
