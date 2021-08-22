from pre_process_utils import convert_origin_2_raw_data, convert_raw_data_2_data_frame, convert_df_2_pkl, \
  bert_w2v_mapper, finally_concat_pickles
import create_vectors_text_meta_voice, hparam, new_d_vectors2, kmeans_m
import get_predictions
from hparam import hparam as hp
import settings

def main():
  settings.init()  
  convert_origin_2_raw_data()
  convert_raw_data_2_data_frame()
  convert_df_2_pkl()
  bert_w2v_mapper()
  finally_concat_pickles()
  create_vectors_text_meta_voice.create_vectors_from_preprocessed_data()
  get_predictions.get_predictions_start()
  new_d_vectors2.run_D_vectors()
  kmeans_m.startk()
  return


def get_kmeans_data():
    settings.init()
    return kmeans_m.start()


def pre_process():
    settings.init()
    convert_origin_2_raw_data()
    convert_raw_data_2_data_frame()
    convert_df_2_pkl()
    bert_w2v_mapper()
    finally_concat_pickles()
    return


def first_process():
    settings.init()
    create_vectors_text_meta_voice.create_vectors_from_preprocessed_data()
    get_predictions.get_predictions_start()
    return


def second_process():
    settings.init()
    new_d_vectors2.run_D_vectors()
    return kmeans_m.start()




def startSpreProcess():
    return pre_process()


def startFirstProcess():
    return first_process()


def startSecondProcess():
    return second_process()

if __name__ == "__main__":
    main()

