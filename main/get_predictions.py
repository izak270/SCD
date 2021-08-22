import os
import torch
import numpy as np
import pandas as pd
import xlsxwriter

import glob
from pathlib import Path
from time import gmtime, strftime
import settings
from hybrid_bert_nn_definition import HybridSCDModel


#in this part we use the model / models we have to predict if if it's the same speaker or not between each two words


LABEL_INDEX = 2063

file_name = "Bmr030"


def get_predictions(general_df, words_vectors):

    words_size = len(general_df)

    all_words_with_predictions = pd.DataFrame(index=range((words_size)),
                                columns=["Word", "From", "To", "Label", "Speaker"])
    
    for j in range (words_size ):
      all_words_with_predictions["Word"].iloc[j] = general_df.iloc[j]["Word"]
      all_words_with_predictions["From"].iloc[j] = general_df.iloc[j]["From"]
      all_words_with_predictions["To"].iloc[j] = general_df.iloc[j]["To"]
      all_words_with_predictions["Speaker"].iloc[j] = general_df.iloc[j]["Speaker"]


    all_words_with_predictions["Label"].iloc[0] = "Same"
    all_words_with_predictions["Label"].iloc[1] = "Same"
    all_words_with_predictions["Label"].iloc[words_size -1] = "Same"
    all_words_with_predictions["Label"].iloc[words_size -2] = "Same"
    all_words_with_predictions["Label"].iloc[words_size -3] = "Same"
    all_words_with_predictions["Label"].iloc[words_size -4] = "Same"

  
    test_vectors =  words_vectors

    X_test = test_vectors.iloc[:, :-2]
    Y_test = list(test_vectors[LABEL_INDEX])

    classes = pd.read_pickle(settings.PATH + 'Pickles/hybrid_BERT_classes_for_test.pkl')
    inverse_classes = {v: k for k, v in classes.items()}

    data_x = []
    indices = X_test.index.values

    idx = 0
    for index in indices:
        idx += 1
        data_x.append(list(X_test.loc[index]))

    test_x = np.array(data_x)
    torch_tensor_X = torch.from_numpy(test_x).float()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    device = "cpu"

    os.chdir(settings.PATH + "Models/Neural/")
    all_models_name = glob.glob("*.pth")
    all_models_name.sort(key=lambda x: os.PATH.getmtime(x))

    results = []

    print(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))

    for k in range(len(all_models_name)):

        curr_y_pred = []
        curr_y_true = []

        #  y_probas = []

        split_rate = 0
        split_pred = 0
        same_rate = 0
        same_pred = 0

        model_name = all_models_name[k]
        filename = Path(settings.PATH + "Models/Neural/" + model_name)

        model = torch.load(filename, map_location=device)
        model.eval()
        model.cpu()
        print(str(k + 1) + ", Model " + model_name + " has restored at " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))

        model.eval()
        inputs = torch_tensor_X.to(device)
        predictions = model.forward(inputs)

        for i in range(len(predictions)):
            prediction = predictions[i]
            prediction = [prediction.data[0].item(), prediction.data[1].item()]
            prediction = [round(x, 3) for x in prediction]
            #  y_probas.append(prediction)

            true_class = Y_test[i]
            max_index = prediction.index(max(prediction))
            prediction_class = inverse_classes[max_index]
            all_words_with_predictions["Label"].iloc[i+2] = prediction_class

            curr_y_pred.append(prediction_class)
            curr_y_true.append(true_class)

    fileName = settings.PATH + "/Excels/All_Words_With_Speaker_And_Label.xlsx"
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.set_column(0, 5, 15)

    worksheet.write(0, 0, "Word", bold)
    worksheet.write(0, 1, "Start Time", bold)
    worksheet.write(0, 2, "End Time", bold)
    worksheet.write(0, 3, "Label", bold)
    worksheet.write(0, 4, "Speaker", bold)

    for k in range(len(all_words_with_predictions)):
      for j in range(0, 5):
        try: 
          worksheet.write((k + 1), j, all_words_with_predictions.iloc[k][j])
        except:
          pass

    print("Created All_Words_With_Speaker_And_Label.xlsx in Excels folder - all words with true speaker and predicted label")
    workbook.close()
    return all_words_with_predictions 

def get_predictions_start():

  print("Start to use in model to get predictions labels")
  general_df = pd.read_pickle(settings.PATH + "Pickles/general_df_4_all_files.pkl") # read the all-words file (including identity)
  words_vectors = pd.read_pickle(settings.PATH + "Pickles/vec/prepared_vectors_2_split-" + file_name + ".pkl") # load the matched vectors 
  all_words_with_predictions = get_predictions(general_df, words_vectors) # get the predictions file
  pd.to_pickle(all_words_with_predictions, settings.PATH + "Pickles/" + file_name +"_with_labels" + ".pkl")
  print("Done with labels for all words - saved in " + settings.PATH + "Pickles/" + file_name +"_with_labels" + ".pkl")
	
  return 