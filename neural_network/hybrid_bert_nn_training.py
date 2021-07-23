import torch
import torch.nn as nn
from torch import optim
import numpy as np
import pandas as pd
from time import gmtime, strftime
from SCD.ICSI_Dataset.Code.neural_network.hybrid_bert_nn_definition import HybridSCDModel


DIMENSION = 2062

LABEL_INDEX = 2063

PATH = "/home/user/IdeaProjects/libonea/demos/SCD/ICSI_Dataset/"


def get_classes(l):

    class_dict = {}
    l = sorted(list(set(list([str(x) for x in l]))))

    for i in range(len(l)):
        class_dict.update({l[i]: i})

    return class_dict


def get_tensors_x_y(x_t, y_t, cls):
    data_x = []
    data_y = []

    indices = x_t.index.values

    idx = 0
    for index in indices:
        idx += 1
        print(str(idx) + " out of: " + str(len(indices)))
        data_x.append(list(x_t.loc[index]))
        data_y.append(cls[y_t[index]])

    torch_tensor_X = torch.from_numpy(np.array(data_x))
    torch_tensor_Y = torch.from_numpy(np.array(data_y))

    return torch_tensor_X, torch_tensor_Y


train_vectors = pd.read_pickle(PATH + 'Pickles/ICSI-Hybrid_Data_Vectors-Speech-NLP_Train.pkl')

print("Done read vectors " + str(len(train_vectors)))

split_examples = len(train_vectors[train_vectors[LABEL_INDEX] == "Split"])
same_examples = len(train_vectors[train_vectors[LABEL_INDEX] == "Same"])

X_train = train_vectors.iloc[:, :-2]
Y_train = train_vectors[LABEL_INDEX]
classes = get_classes(Y_train)

pd.to_pickle(classes, PATH + "Pickles/hybrid_BERT_classes_for_test.pkl")

print("Getting tensors")
X, Y = get_tensors_x_y(X_train, Y_train, classes)
print("Done getting tensors")

X = X.float()
Y = Y.long()

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = HybridSCDModel().to(device)
learning_rate = model.get_learning_rate()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

weights = [1.0 / same_examples, 1.0 / split_examples]

class_weights = torch.FloatTensor(weights).cuda()

criterion = nn.CrossEntropyLoss(weight=class_weights)

batch_size = 5000
batch_number = int(len(train_vectors) / batch_size) + 1

steps = model.get_steps()

for i in range(steps):
    model.train()
    optimizer.zero_grad()

    mod = i % batch_number
    if (batch_number - 1) == mod:
        index_batch_min = mod * batch_size
        index_batch_max = len(X) - 1
    else:
        index_batch_min = mod * batch_size
        index_batch_max = (mod + 1) * batch_size

    x_to_device = X[index_batch_min:index_batch_max]
    y_to_device = Y[index_batch_min:index_batch_max]

    y_ = model(x_to_device.to(device))
    loss = criterion(y_, y_to_device.to(device))
    loss.backward()
    optimizer.step()

    print("Step: " + str(i+1) + ",  Loss Function: " + str(loss) +
          ",  From: " + str(index_batch_min) + ",  to: " + str(index_batch_max))

    if 0 == (i+1) % 100:
        print(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))

    if 0 == i % 200:
        torch.save(model, PATH + "Models/Neural/" + model.to_string() + str(i) + ".pth")

torch.save(model, PATH + "Models/Neural/" + model.to_string() + str(steps) + ".pth")

pass
