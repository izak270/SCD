import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


fixPATH = "/home/imanuel/Documents/SCD/ICSI_Dataset/"


class WordObject:
    def __init__(self, fn, w, start, end, speaker):
        self.file_name = fn
        self.word = w
        self.start_time = start
        self.end_time = end
        self.speaker = speaker


os.chdir(PATH + "Data/ICSI_plus_NXT/Words") #current path
all_file_name = glob.glob("*.xml")# returns a list of all files that matches the "*.xml" pattern
all_file_name.sort(key=lambda x: os.path.getmtime(x)) # sort the files by the time they were last changed

files = [x.split(".")[0] for x in all_file_name] #for all the file names array take the first string from the file names
files = sorted(list(set(list(files)))) # takes the unique file name

files_set = {}
for key in files:
    files_set.update({key: []})

err_count = 0

for f_name in all_file_name: # iterate on all files

    file_words = []

    tree = ET.parse(PATH + "Data/ICSI_plus_NXT/Words/" + f_name)
    root = tree.getroot()

    file_id = f_name.split(".")[0] # unique file name
    file_speaker = f_name.split(".")[1] # the speaker from file name

    if len(file_speaker) > 0:  # because of the file Buw001..words that has no speaker
        for child in root:
            tag = child.tag
            attribute = child.attrib

            if 'w' == tag:
                if attribute['c'] == 'W':
                    word = child.text # take the word

                    try:
                        start_time = float(attribute['starttime'])
                        end_time = float(attribute['endtime'])
                    except:
                        continue #skip on words without start and end time

                        # err_count += 1
                        # if "" == attribute['starttime']:
                            # start_time = float(attribute['endtime']) - 0.3
                        # if "" == attribute['endtime']:
                            # end_time = float(attribute['starttime']) + 0.3

                    word_to_add = WordObject(file_id, word, start_time, end_time, file_speaker) # if all fields are ok create an object
                    file_words.append(word_to_add) # add the object to a list

        files_set[file_id].append(file_words)
# files_set is a dictionary of file names = keys and lists where the list are all words as objects (id, start, end, word)
pd.to_pickle(files_set, PATH + "Pickles/files_df.pkl") # from list of lists to pickle file

pass
