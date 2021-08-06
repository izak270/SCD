import itertools
import pandas as pd


PATH = "/home/imanuel/Documents/SCD/ICSI_Dataset/"


class WordObject:
    def __init__(self, fn, w, start, end, speaker):
        self.file_name = fn
        self.word = w
        self.start_time = start
        self.end_time = end
        self.speaker = speaker


raw_data = pd.read_pickle(PATH + "Pickles/files_df.pkl") # from pickle to list of lists

general_df = pd.DataFrame(columns=["ID", "Word", "From", "To", "Speaker"]) # initialize new data frame object with the specified column names

count = 0
size = len(raw_data.keys()) # key is the file name. size is how many files we have in the dictionary

for file_key in raw_data.keys():

    speakers_value = raw_data[file_key] # get all values of current file
    concatenated_speakers_list = sum(speakers_value, []) # get one list - which is the sum of all lists
    concatenated_speakers_list = sorted(concatenated_speakers_list, key=lambda x: x.start_time, reverse=False) # sort the list by the start time

    curr_file_df = pd.DataFrame(index=range(len(concatenated_speakers_list)),
                                columns=["ID", "Word", "From", "To", "Speaker"])
# initialize a data frame and iterate over the concatenated list and add the value to the data frame
    for i in range(len(concatenated_speakers_list)):
        word_obj = concatenated_speakers_list[i]

        curr_file_df["ID"].iloc[i] = word_obj.file_name
        curr_file_df["Word"].iloc[i] = word_obj.word
        curr_file_df["From"].iloc[i] = word_obj.start_time
        curr_file_df["To"].iloc[i] = word_obj.end_time
        curr_file_df["Speaker"].iloc[i] = word_obj.speaker

    count += 1
    general_df = pd.concat([general_df, curr_file_df], ignore_index=True) # add the current file data frame to the general data frame
    print("Done " + str(count) + " files, out of: " + str(size))

print("Original Length: " + str(len(general_df))) # print the length of the general data frame - all inserted files
general_df = general_df.dropna()#dropna = drop not available
print("After dropna Length: " + str(len(general_df)))

pd.to_pickle(general_df, PATH + "Pickles/general_df_4_all_files.pkl") # from data frame to pickle

pass
