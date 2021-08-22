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

def startMain():
    return main()
#
if __name__ == "__main__":
    main()

