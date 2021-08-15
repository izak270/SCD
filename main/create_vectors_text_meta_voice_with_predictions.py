import os
import torch
import librosa
import numpy as np
import pandas as pd
from pydub import AudioSegment
from time import gmtime, strftime

import glob
from pathlib import Path

from hparam import hparam as hp
from VAD_segments import VAD_chunk
from speech_embedder_net import SpeechEmbedder


PATH = "/home/itzhak/SCD/"

WAV_PATH = "Signals/"

W2V_VECTOR_LENGTH = 768

SPEECH_EMBEDDING_DIMENSION = 256

LABEL_INDEX = 2063


def concat_segs(times, segs):
    # Concatenate continuous voiced segments
    concat_seg = []
    concat_times = []
    seg_concat = segs[0]
    for i in range(0, len(times) - 1):
        if times[i][1] == times[i + 1][0]:
            seg_concat = np.concatenate((seg_concat, segs[i + 1]))
        else:
            concat_seg.append(seg_concat)
            seg_concat = segs[i + 1]
    else:
        concat_seg.append(seg_concat)

    curr_start = times[0][0]
    for i in range(0, len(times) - 1):
        if times[i][1] != times[i + 1][0]:
            curr_touple = (curr_start, times[i][1])
            curr_start = times[i + 1][0]
            concat_times.append(curr_touple)
    last_touple = (curr_start, times[-1][1])
    concat_times.append(last_touple)

    return concat_seg


def get_STFTs(segs):
    #Get 240ms STFT windows with 50% overlap
    sr = hp.data.sr
    STFT_frames = []
    for i in range(len(segs)):
        seg = segs[i]
        if(0 == len(seg)):
            break
        S = librosa.core.stft(y=seg, n_fft=hp.data.nfft,
                              win_length=int(hp.data.window * sr), hop_length=int(hp.data.hop * sr))
        S = np.abs(S)**2
        mel_basis = librosa.filters.mel(sr, n_fft=hp.data.nfft, n_mels=hp.data.nmels)
        S = np.log10(np.dot(mel_basis, S) + 1e-6)           # log mel spectrogram of utterances
        for j in range(0, S.shape[1], int(.12/hp.data.hop)):
            if j + 24 < S.shape[1]:
                STFT_frames.append(S[:,j:j+24])
            else:
                break
    return STFT_frames


def align_embeddings(embeddings):
    partitions = []
    start = 0
    end = 0
    j = 1
    for i, embedding in enumerate(embeddings):
        if (i*.12)+.24 < j*.401:
            end = end + 1
        else:
            partitions.append((start,end))
            start = end
            end = end + 1
            j += 1
    else:
        partitions.append((start,end))
    avg_embeddings = np.zeros((len(partitions),256))
    for i, partition in enumerate(partitions):
        avg_embeddings[i] = np.average(embeddings[partition[0]:partition[1]],axis=0)
    return avg_embeddings


def get_average_voice_embedding(path_to_audio):

    times, segs = VAD_chunk(2, path_to_audio)
    if segs == []:
        return ""

    concat_seg = concat_segs(times, segs)
    STFT_frames = get_STFTs(concat_seg)
    STFT_frames = np.stack(STFT_frames, axis=2)
    STFT_frames = torch.tensor(np.transpose(STFT_frames, axes=(2, 1, 0)))
    embeddings = embedder_net(STFT_frames)
    aligned_embeddings = align_embeddings(embeddings.detach().numpy())

    return aligned_embeddings


def get_half_embedding(segment_start, segment_end, the_wav):

    seg_start = float(segment_start) * 1000  # Works in milliseconds
    seg_end = float(segment_end) * 1000

    sub_sample = the_wav[seg_start:seg_end]
    file_2_create = PATH + "temp_wav_file.wav"
    sub_sample.export(file_2_create, format="wav")

    voice_embedding_vectors = get_average_voice_embedding(file_2_create)

    os.remove(file_2_create)

    avg_vector = np.zeros(SPEECH_EMBEDDING_DIMENSION)
    for embedding in voice_embedding_vectors:
        avg_vector += embedding
    avg_vector = avg_vector / len(voice_embedding_vectors)

    return avg_vector


def create_vectors(df, w2v):

    vectors_pkl = pd.DataFrame(index=range(len(df)), columns=range(1, 2 * W2V_VECTOR_LENGTH +
                                                                   2 * SPEECH_EMBEDDING_DIMENSION + 17)) #rows = words, columns = 2064
    random = 0

    last_seen_file_id = ""
    last_seen_wav_file = ""

    all_words_with_predictions = pd.DataFrame(index=range((len(df))),
                                columns=["Word", "From", "To", "Label"])

    for i in range (len(df)):
        try:

            file_id = df.iloc[i]["ID"]


            all_words_with_predictions["Word"].iloc[i] = df.iloc[i]["First_Word"]
            all_words_with_predictions["From"].iloc[i] = df.iloc[i]["Segment_Start"]
            all_words_with_predictions["To"].iloc[i] = df.iloc[i]["Segment_Start"] + df.iloc[i]["First_Duration"]

            # NLP embedding for first half of the sliding window
            first_vec = np.zeros(W2V_VECTOR_LENGTH) # array. size: 768. values: 0
            num_words_1 = 0

            first_sent = list(df.iloc[i][1:4]) # start with 3 first words

            for word in first_sent: # iterate on the 3 words
                original_vector = w2v[word] # get bert vector for current word
                first_vec += original_vector # add bert vector of current word to the first vector
                num_words_1 += 1

            if num_words_1 == 3:
                vectors_pkl.iloc[i][0:W2V_VECTOR_LENGTH] = first_vec / num_words_1
            else:
                random += 1

            # calculus of second vector
            second_vec = np.zeros(W2V_VECTOR_LENGTH)
            num_words_2 = 0

            second_sent = list(df.iloc[i][4:7])

            for word in second_sent:
                original_vector = w2v[word]
                second_vec += original_vector
                num_words_2 += 1

            if num_words_2 == 3:
                vectors_pkl.iloc[i][W2V_VECTOR_LENGTH: 2 * W2V_VECTOR_LENGTH] = second_vec / num_words_2
            else:
                random += 1

            #################-SPEECH-#################
            if file_id != last_seen_file_id:
                last_seen_file_id = file_id
                last_seen_wav_file = AudioSegment.from_wav(PATH + WAV_PATH +
                                                           "/" + str(file_id) + ".interaction.wav")

            # speech embedding for first half of the sliding window
            seg_start_first = df.iloc[i]["Segment_Start"]
            seg_end_first = df.iloc[i]["Segment_Middle_1"]
            avg_vector_first = get_half_embedding(seg_start_first, seg_end_first, last_seen_wav_file)

            # speech embedding for second half of the sliding window
            seg_start_second = df.iloc[i]["Segment_Middle_2"]
            seg_end_second = df.iloc[i]["Segment_End"]
            avg_vector_second = get_half_embedding(seg_start_second, seg_end_second, last_seen_wav_file)

            nlp_end_index = 2 * W2V_VECTOR_LENGTH

            vectors_pkl.iloc[i][nlp_end_index: nlp_end_index + SPEECH_EMBEDDING_DIMENSION] = avg_vector_first
            vectors_pkl.iloc[i][nlp_end_index + SPEECH_EMBEDDING_DIMENSION:
                                nlp_end_index + 2 * SPEECH_EMBEDDING_DIMENSION] = avg_vector_second

            meta_data_start_index = nlp_end_index + 2 * SPEECH_EMBEDDING_DIMENSION

            vectors_pkl.iloc[i][meta_data_start_index + 1] = df.iloc[i]["First_Duration"]
            vectors_pkl.iloc[i][meta_data_start_index + 2] = df.iloc[i]["Second_Duration"]
            vectors_pkl.iloc[i][meta_data_start_index + 3] = df.iloc[i]["Third_Duration"]
            vectors_pkl.iloc[i][meta_data_start_index + 4] = df.iloc[i]["Fourth_Duration"]
            vectors_pkl.iloc[i][meta_data_start_index + 5] = df.iloc[i]["Fifth_Duration"]
            vectors_pkl.iloc[i][meta_data_start_index + 6] = df.iloc[i]["Sixth_Duration"]
            vectors_pkl.iloc[i][meta_data_start_index + 7] = df.iloc[i]["First_Normal"]
            vectors_pkl.iloc[i][meta_data_start_index + 8] = df.iloc[i]["Second_Normal"]
            vectors_pkl.iloc[i][meta_data_start_index + 9] = df.iloc[i]["Third_Normal"]
            vectors_pkl.iloc[i][meta_data_start_index + 10] = df.iloc[i]["Fourth_Normal"]
            vectors_pkl.iloc[i][meta_data_start_index + 11] = df.iloc[i]["Fifth_Normal"]
            vectors_pkl.iloc[i][meta_data_start_index + 12] = df.iloc[i]["Sixth_Normal"]
            vectors_pkl.iloc[i][meta_data_start_index + 13] = df.iloc[i]["Space_3_4"]

            vectors_pkl.iloc[i][meta_data_start_index + 14] = np.linalg.norm(avg_vector_first - avg_vector_second)

            vectors_pkl.iloc[i][meta_data_start_index + 15] = df.iloc[i]["Label"]
            vectors_pkl.iloc[i][meta_data_start_index + 16] = df.iloc[i]["ID"]

            if i % 100 == 0:
                print(str(i) + "  " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + "  ,  Random is: " + str(random))
            else:
                print("Index: " + str(i) + " Out of: " + str(len(df)))

        except Exception as e:
            random += 1
            print("Error in reading row: " + str(i) + ", " + str(e))
            continue

    print("Random Vectors: " + str(random))


    test_vectors =  vectors_pkl

    X_test = test_vectors.iloc[:, :-2]
    Y_test = list(test_vectors[LABEL_INDEX])

    classes = pd.read_pickle(PATH + 'Pickles/hybrid_BERT_classes_for_test.pkl')
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

    os.chdir(PATH + "Models/Neural/")
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
        filename = Path(PATH + "Models/Neural/" + model_name)

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
            all_words_with_predictions["Label"].iloc[i] = prediction_class

            curr_y_pred.append(prediction_class)
            curr_y_true.append(true_class)

    pd.to_pickle(all_words_with_predictions, PATH + "Pickles/"+file_id+"_with_labels"+".pkl")
    return vectors_pkl

def create_labels_df_from_vectors():

  data_df = pd.read_pickle(PATH + "Pickles/raw_data_2_convert_2_embeddings.pkl") # load the final data frame (ordered by segments)

  id_list = sorted(list(set(list(data_df["ID"])))) # extract all file names from the data frame
  # id_list = id_list[24:]

  word2vec = pd.read_pickle(PATH + 'Models/Word2Vec/bert_w2v_dictionary.pkl') # bert dictionary for each word -> list of 768 values

  for curr_id in id_list:
      sub_df = data_df[data_df["ID"] == curr_id] # sub data frame splitted according to the current file name
      curr_data = create_vectors(sub_df, word2vec) #
      pd.to_pickle(curr_data, PATH + "Pickles/vec/prepared_vectors_2_split-" + str(curr_id) + ".pkl")
  return


embedder_net = SpeechEmbedder()
embedder_net.load_state_dict(torch.load(hp.model.model_path)) # we load the model specified in the config file - final_epoch_950_batch_id_141.model
embedder_net.eval()

# data_df = pd.read_pickle(PATH + "Pickles/raw_data_2_convert_2_embeddings.pkl") # load the final data frame (ordered by segments)
#
# id_list = sorted(list(set(list(data_df["ID"])))) # extract all file names from the data frame
# # id_list = id_list[24:]
#
# word2vec = pd.read_pickle(PATH + 'Models/Word2Vec/bert_w2v_dictionary.pkl') # bert dictionary for each word -> list of 768 values
#
# for curr_id in id_list:
#     sub_df = data_df[data_df["ID"] == curr_id] # sub data frame splitted according to the current file name
#     curr_data = create_vectors(sub_df, word2vec) #
#     pd.to_pickle(curr_data, PATH + "Pickles/vec/prepared_vectors_2_split-" + str(curr_id) + ".pkl")
#
# pass
