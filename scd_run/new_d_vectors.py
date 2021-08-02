import os
import torch
import librosa
import numpy as np
import pandas as pd
from pydub import AudioSegment
from time import gmtime, strftime

from hparam import hparam as hp
from VAD_segments import VAD_chunk
from speech_embedder_net import SpeechEmbedder

# TODO: talk with other groups about files addresses & data saving conv
# TODO: change addresses
PATH = ""

WAV_PATH = ""

W2V_VECTOR_LENGTH = 768

SPEECH_EMBEDDING_DIMENSION = 256


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
    # Get 240ms STFT windows with 50% overlap
    sr = hp.data.sr
    STFT_frames = []
    for i in range(len(segs)):
        seg = segs[i]
        if (0 == len(seg)):
            break
        S = librosa.core.stft(y=seg, n_fft=hp.data.nfft,
                              win_length=int(hp.data.window * sr), hop_length=int(hp.data.hop * sr))
        S = np.abs(S) ** 2
        mel_basis = librosa.filters.mel(sr, n_fft=hp.data.nfft, n_mels=hp.data.nmels)
        S = np.log10(np.dot(mel_basis, S) + 1e-6)  # log mel spectrogram of utterances
        for j in range(0, S.shape[1], int(.12 / hp.data.hop)):
            if j + 24 < S.shape[1]:
                STFT_frames.append(S[:, j:j + 24])
            else:
                break
    return STFT_frames


def align_embeddings(embeddings):
    partitions = []
    start = 0
    end = 0
    j = 1
    for i, embedding in enumerate(embeddings):
        if (i * .12) + .24 < j * .401:
            end = end + 1
        else:
            partitions.append((start, end))
            start = end
            end = end + 1
            j += 1
    else:
        partitions.append((start, end))
    avg_embeddings = np.zeros((len(partitions), 256))
    for i, partition in enumerate(partitions):
        avg_embeddings[i] = np.average(embeddings[partition[0]:partition[1]], axis=0)
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
    #TODO: change size of df! Changed to vector+2 for start/end time
    vectors_pkl = pd.DataFrame(index=range(len(df)), columns=range(1, W2V_VECTOR_LENGTH +
                                                                   SPEECH_EMBEDDING_DIMENSION + 2))
    random = 0

    last_seen_file_id = ""
    last_seen_wav_file = ""
    for i in range(len(df)):
        try:
            index_label = i
            file_id = df.iloc[i]["ID"]

            # NLP embedding for first half of the sliding window

            # /////////////////////////////first_vec = np.zeros(W2V_VECTOR_LENGTH)

            #t_Label = df.iloc[i]["Label"]

            #first_sent = list(df.iloc[i][1:4])

            while i < range(len(df)) and df.iloc[i]["Label"] != "Split":
                i += 1

            # TODO: change labels as Mano & Revital saving it

            seg_start_first = df.iloc[index_label]["Start_Time"]
            seg_end_first = df.iloc[i]["End_Time"]

            '''
            for word in first_sent:
                original_vector = w2v[word]
                first_vec += original_vector
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
'''
            #################-SPEECH-#################
            if file_id != last_seen_file_id:
                last_seen_file_id = file_id
                last_seen_wav_file = AudioSegment.from_wav(PATH + WAV_PATH +
                                                           str(file_id) + "/" + str(file_id) + ".interaction.wav")

            # speech embedding for first half of the sliding window
            # seg_start_first = df.iloc[i]["Segment_Start"]
            # seg_end_first = df.iloc[i]["Segment_End"]
            #TODO: it's more than one "last_seen_wav_file" How data saved? Is it splited to many wav files or wav file its one record?
            avg_vector_first = get_half_embedding(seg_start_first, seg_end_first, last_seen_wav_file)

            #nlp_end_index = (i - index_label) * W2V_VECTOR_LENGTH
            nlp_end_index = W2V_VECTOR_LENGTH

            vectors_pkl.iloc[i][nlp_end_index: nlp_end_index + SPEECH_EMBEDDING_DIMENSION] = avg_vector_first
            #vectors_pkl.iloc[i][nlp_end_index + SPEECH_EMBEDDING_DIMENSION:
            #                    nlp_end_index + 2 * SPEECH_EMBEDDING_DIMENSION] = avg_vector_second

            meta_data_start_index = nlp_end_index + SPEECH_EMBEDDING_DIMENSION

            vectors_pkl.iloc[i][meta_data_start_index + 1] = seg_start_first
            vectors_pkl.iloc[i][meta_data_start_index + 2] = seg_end_first

            '''
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
            '''

            if i % 100 == 0:
                print(str(i) + "  " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + "  ,  Random is: " + str(random))
            else:
                print("Index: " + str(i) + " Out of: " + str(len(df)))

        except Exception as e:
            random += 1
            print("Error in reading row: " + str(i) + ", " + str(e))
            continue

    print("Random Vectors: " + str(random))

    return vectors_pkl


embedder_net = SpeechEmbedder()
embedder_net.load_state_dict(torch.load(hp.model.model_path))
embedder_net.eval()

# TODO: change addresses
data_df = pd.read_pickle(PATH + "Pickles/raw_data_2_convert_2_embeddings.pkl")

id_list = sorted(list(set(list(data_df["ID"]))))
# id_list = id_list[24:]

word2vec = pd.read_pickle(PATH + 'Models/Word2Vec/bert_w2v_dictionary.pkl')

for curr_id in id_list:
    sub_df = data_df[data_df["ID"] == curr_id]
    curr_data = create_vectors(sub_df, word2vec)
    pd.to_pickle(curr_data, PATH + "Pickles/vec/prepared_vectors" + str(curr_id) + ".pkl")
pass
