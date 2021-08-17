import os
import torch
import librosa
import numpy as np
import pandas as pd
import  time
from pydub import AudioSegment
from time import gmtime, strftime

from hparam import hparam as hp
from VAD_segments import VAD_chunk
from speech_embedder_net import SpeechEmbedder

# TODO: talk with other groups about files addresses & data saving conv
# TODO: change addresses
PATH = "/home/itzhak/SCD/"
PICKLE_PATH = "Pickles/Bed003_with_labels.pkl"
WAV_PATH = "Signals/"
WAV_NAME = "Bed003.interaction.wav"

FINALE_PICKLE_NAME = "RON_OLGA"

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


def create_vectors(df):
    #vectors_pkl = pd.DataFrame(index=range(len(df)), columns=range(4))
    random = 0
    j=-1
    # size = 60
    size = len(df)
    vectors_pkl = pd.DataFrame(index = range(size), columns=["From", "To", "Vectors"])
    index_label = 0
    last_seen_wav_file = AudioSegment.from_wav(PATH + WAV_PATH + WAV_NAME)
    for i in range(size):
      
      try:  
        if df.iloc[i]["Label"] == "Split":
          # TODO: change labels as Mano & Revital saving it
          seg_start_first = df.iloc[index_label]["From"]
          seg_end_first = df.iloc[i]["To"]
          index_label = i+1
          j= j+1
          vectors_pkl.iloc[j][0] = seg_start_first
          vectors_pkl.iloc[j][1] = seg_end_first
          avg_vector_first = get_half_embedding(seg_start_first, seg_end_first, last_seen_wav_file)
          vectors_pkl.iloc[j][2] = avg_vector_first

      except Exception as e:
        random += 1
        continue

    if df.iloc[size-1]["Label"] == "Same":
      seg_start_first = df.iloc[index_label]["From"]
      seg_end_first = df.iloc[size-1]["To"]
      vectors_pkl.iloc[j+1][0] = seg_start_first
      vectors_pkl.iloc[j+1][1] = seg_end_first
      avg_vector_first = get_half_embedding(seg_start_first, seg_end_first, last_seen_wav_file)
      vectors_pkl.iloc[j+1][2] = avg_vector_first

    print("Random Vectors: " + str(random))

    return vectors_pkl


def run_D_vectors():
    data_df = pd.read_pickle(PATH + PICKLE_PATH)
    curr_data = create_vectors(data_df)
    pd.to_pickle(curr_data, PATH + "Pickles/vec/prepared_vectors_2_split-" + FINALE_PICKLE_NAME + ".pkl")
    # data_df2 = pd.read_pickle(PATH + "Pickles/vec/prepared_vectors_2_split-" + FINALE_PICKLE_NAME + ".pkl")
    # print(data_df2.to_string())
    return

embedder_net = SpeechEmbedder()
embedder_net.load_state_dict(torch.load(hp.model.model_path))
embedder_net.eval()




