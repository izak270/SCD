import pandas as pd
from time import gmtime, strftime
import torch
import numpy as np
import xlsxwriter
import glob, os
from pathlib import Path
from sklearn.metrics import precision_recall_fscore_support


DIMENSION = 2062

LABEL_INDEX = 2063

PATH = "/home/user/IdeaProjects/libonea/demos/SCD/ICSI_Dataset/"


test_vectors = pd.read_pickle(PATH + 'Pickles/ICSI-Hybrid_Data_Vectors-Speech-NLP_Test.pkl')

X_test = test_vectors.iloc[:, :-2]
Y_test = list(test_vectors[LABEL_INDEX])

classes = pd.read_pickle(PATH + 'Pickles/hybrid_BERT_classes_for_test.pkl')
inverse_classes = {v: k for k, v in classes.items()}

data_x = []
indices = X_test.index.values

idx = 0
for index in indices:
    idx += 1
    print(str(idx) + " out of: " + str(len(indices)))
    data_x.append(list(X_test.loc[index]))

test_x = np.array(data_x)
torch_tensor_X = torch.from_numpy(test_x).float()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device = "cpu"

os.chdir(PATH + "Models/Neural")
all_models_name = glob.glob("*.pth")
all_models_name.sort(key=lambda x: os.path.getmtime(x))

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
    filename = Path(PATH + "Models/" + model_name)
    model = torch.load(filename.name, map_location=device)
    model.eval()
    model.cpu()
    print(str(k+1) + ", Model " + model_name + " has restored at " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))

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

        curr_y_pred.append(prediction_class)
        curr_y_true.append(true_class)

        if 'Split' == true_class:
            split_rate += 1
            if 'Split' == prediction_class:
                split_pred += 1

        if 'Same' == true_class:
            same_rate += 1
            if 'Same' == prediction_class:
                same_pred += 1

    accuracy = precision_recall_fscore_support(curr_y_true, curr_y_pred, average='weighted')
    precision = accuracy[0]
    recall = accuracy[1]
    f_score = accuracy[2]
    # confusion_mat = confusion_matrix(curr_y_true, curr_y_pred)
    # roc_auc = skplt.metrics.plot_roc_curve(list(curr_y_true), y_probas)

    split_proportion = float(split_pred) / float(split_rate)
    same_proportion = float(same_pred) / float(same_rate)

    results.append([str(model_name),
                    str(round(precision * 100, 3)),
                    str(round(recall * 100, 3)),
                    str(round(f_score * 100, 3)),
                    str(round(split_proportion * 100, 3)),
                    str(round(same_proportion * 100, 3))])

pd.to_pickle(results, PATH + "Results/Model_Results_With_Statistics.pkl")
print(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


fileName = PATH + "Results/Models_all_data.xlsx"
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.set_column(0, 6, 15)

worksheet.write(0, 0, "Model Name", bold)
worksheet.write(0, 1, "Precision", bold)
worksheet.write(0, 2, "Recall", bold)
worksheet.write(0, 3, "F1-Score", bold)
worksheet.write(0, 4, "Split Rate Success", bold)
worksheet.write(0, 5, "Same Rate Success", bold)

for k in range(len(results)):
    for j in range(0, len(results[0])):
        worksheet.write((k + 1), j, results[k][j])

workbook.close()

pass
