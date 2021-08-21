import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import itertools
from time import gmtime, strftime
from bert_embedding import BertEmbedding
from pathlib import Path
import xlsxwriter

PATH = "/home/itzhak/SCD/"

class WordObject:
    def __init__(self, fn, w, start, end, speaker):
        self.file_name = fn
        self.word = w
        self.start_time = start
        self.end_time = end
        self.speaker = speaker

def convert_origin_2_raw_data():
  os.chdir(PATH + "words") #current path
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

      tree = ET.parse(PATH + "words/" + f_name)
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
  print("Finish with origin")
  return

def convert_raw_data_2_data_frame():
  print("start with raw data")
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
  
  fileName = PATH + "Excels/current_run_all_words_and_speakers.xlsx"
  workbook = xlsxwriter.Workbook(fileName)
  worksheet = workbook.add_worksheet()
  bold = workbook.add_format({'bold': True})
  worksheet.set_column(0, 5, 15)
    
  columns_names= ['ID', 'WORD', 'FROM', 'TO', 'SPEAKER']

  print(columns_names)

  for r in range(5):
    worksheet.write(0, r, columns_names[r], bold)

  for k in range(len(general_df)):
      for j in range(0, 5):
          worksheet.write((k + 1), j, general_df.iloc[k][j])
  workbook.close()  

  pd.to_pickle(general_df, PATH + "Pickles/general_df_4_all_files.pkl") # from data frame to pickle
  print("Finish with raw data")
  return

def convert_df_2_pkl():
  print("Start with data frame process")
  df = pd.read_pickle(PATH + "Pickles/general_df_4_all_files.pkl")#back to data frame

  id_list = sorted(list(set(df["ID"]))) # extract to list all the file names (from if ID column in the data frame)

  # initilaze a data frame with the specified fields
  data_to_convert_df = pd.DataFrame(columns=['ID', 'First_Word', 'Second_Word', 'Third_Word',
                                           'Fourth_Word', 'Fifth_Word', 'Sixth_Word',
                                           'First_Duration', 'Second_Duration', 'Third_Duration',
                                           'Fourth_Duration', 'Fifth_Duration', 'Sixth_Duration',
                                           'First_Normal', 'Second_Normal', 'Third_Normal',
                                           'Fourth_Normal', 'Fifth_Normal', 'Sixth_Normal',
                                           'Segment_Start', 'Segment_Middle_1', 'Segment_Middle_2', 'Segment_End',
                                           'Space_3_4', 'Label'])
  cntr = 0

  for id in id_list: # for all the file names.
      df_for_id = df[df["ID"] == id] # returns a sub-data-frame where the ID = current file name

      for i in range(len(df_for_id) - 6):
          sub_df = df_for_id[i:i + 6] # return a sub data frame from i row to i+6 row

        # for each sub data frame
        # take the i word, take the duration (end time - start time) and take the normal = time taken to say the word / length of the word

          first_word = str(sub_df.iloc[0]["Word"])
          first_duration = float(sub_df.iloc[0]["To"]) - float(sub_df.iloc[0]["From"])
          first_normal = first_duration / len(first_word)

          second_word = str(sub_df.iloc[1]["Word"])
          second_duration = float(sub_df.iloc[1]["To"]) - float(sub_df.iloc[1]["From"])
          second_normal = second_duration / len(second_word)

          third_word = str(sub_df.iloc[2]["Word"])
          third_duration = float(sub_df.iloc[2]["To"]) - float(sub_df.iloc[2]["From"])
          third_normal = third_duration / len(third_word)

          fourth_word = str(sub_df.iloc[3]["Word"])
          fourth_duration = float(sub_df.iloc[3]["To"]) - float(sub_df.iloc[3]["From"])
          fourth_normal = fourth_duration / len(fourth_word)

          fifth_word = str(sub_df.iloc[4]["Word"])
          fifth_duration = float(sub_df.iloc[4]["To"]) - float(sub_df.iloc[4]["From"])
          fifth_normal = fifth_duration / len(fifth_word)

          sixth_word = str(sub_df.iloc[5]["Word"])
          sixth_duration = float(sub_df.iloc[5]["To"]) - float(sub_df.iloc[5]["From"])
          sixth_normal = sixth_duration / len(sixth_word)


#  two segments:
        #  first segment = words: 1, 2, 3
        # second segment = words: 4, 5, 6
        # segment_start = start time of word number 1
        # segment_middle_1 = end time of word number 3
        # segment_middle_2 = start time of word number 4
        # segment_end = end time of word number 6

          segment_start = sub_df.iloc[0]["From"]
          segment_middle_1 = sub_df.iloc[2]["To"]
          segment_middle_2 = sub_df.iloc[3]["From"]
          segment_end = sub_df.iloc[5]["To"]



          # space_3_4 is the difference between the start of word number 4 to the end of word number 3 - can help as to determine if speakers have changed
          space_3_4 = float(sub_df.iloc[3]["From"]) - float(sub_df.iloc[2]["To"])

          # label is by default: "same" ,but we have all the data and if the speaker between segments is indeed different - label is Split
          label = "Same"
          if str(sub_df.iloc[2]["Speaker"]) != str(sub_df.iloc[3]["Speaker"]):
              label = "Split"

          example_df = pd.DataFrame([[id, first_word, second_word, third_word, fourth_word, fifth_word, sixth_word,
                                    first_duration, second_duration, third_duration,
                                    fourth_duration, fifth_duration, sixth_duration,
                                    first_normal, second_normal, third_normal,
                                    fourth_normal, fifth_normal, sixth_normal,
                                    segment_start, segment_middle_1, segment_middle_2, segment_end,
                                    space_3_4, label]],
                                  columns=data_to_convert_df.columns.values)

          data_to_convert_df = data_to_convert_df.append(example_df) # add the two 2 segments to the general data frame

      cntr += 1
      # print when we finish a file
      print(str(cntr) + " Out of: " + str(len(id_list)) + "    " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))

      # here each 10 files we divide to pickle
      if 0 == cntr % 10:
          pd.to_pickle(data_to_convert_df, PATH + "Pickles/Concat/" + str(cntr) + "-data_to_convert_df_speech_text_hybrid.pkl")

          data_to_convert_df = pd.DataFrame(columns=['ID', 'First_Word', 'Second_Word', 'Third_Word',
                                           'Fourth_Word', 'Fifth_Word', 'Sixth_Word',
                                           'First_Duration', 'Second_Duration', 'Third_Duration',
                                           'Fourth_Duration', 'Fifth_Duration', 'Sixth_Duration',
                                           'First_Normal', 'Second_Normal', 'Third_Normal',
                                           'Fourth_Normal', 'Fifth_Normal', 'Sixth_Normal',
                                           'Segment_Start', 'Segment_Middle_1', 'Segment_Middle_2', 'Segment_End',
                                           'Space_3_4', 'Label'])

  pd.to_pickle(data_to_convert_df, PATH + "Pickles/Concat/" + "last_data_to_convert_df_speech_text_hybrid.pkl")
  print("Finish with data frame process")
  return

def bert_w2v_mapper():
  print("Start to make bert dictionary")
  df = pd.read_pickle(PATH + "Pickles/general_df_4_all_files.pkl") #we take general_df because in general_df... file we have all words ordered in a data frame
  words = sorted(list(set(list(df["Word"])))) # get a list from the data frame under the column Word - a list of all words

  words_dictionary = {}

  bert_embedding = BertEmbedding()

  index = 0
  for word in words:
      result = bert_embedding([word]) # get the value from bert algorithm for current word
      words_dictionary.update({word: result[0][1][0]}) # update the word dictionary: key = word, value = bert value
      index += 1
      print(index)

  pd.to_pickle(words_dictionary, PATH + "Models/Word2Vec/bert_w2v_dictionary.pkl") # a dictionary converted to pickle - to use in the vector part
  print("Finish with Bert dictionary")
  return

def finally_concat_pickles():
  print("Start to concatenate Pickles")
  # list of all files from "convert_df_2_pkl.py" -
  paths = sorted(Path(PATH + "Pickles/Concat/").iterdir(), key=os.path.getmtime)

  # initial_df is the first file
  initial_df = pd.read_pickle(PATH + "Pickles/Concat/" + paths[0].name)

  # here concatenate all file to one final - "raw_data_2_convert_2_embeddings.pkl"
  for i in range(1, len(paths)):
      curr_pkl = pd.read_pickle(PATH + "Pickles/Concat/" + paths[i].name)
      initial_df = pd.concat([initial_df, curr_pkl])# concatenate DFs to initial_df

  pd.to_pickle(initial_df, PATH + "Pickles/raw_data_2_convert_2_embeddings.pkl")
  print("Finish to concatenate Pickles")
  return

 




