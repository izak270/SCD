from pre_process_utils import convert_origin_2_raw_data, convert_raw_data_2_data_frame, convert_df_2_pkl, \
  bert_w2v_mapper, finally_concat_pickles
import create_vectors_text_meta_voice_with_predictions, hparam
from hparam import hparam as hp


def main():
  convert_origin_2_raw_data()
  convert_raw_data_2_data_frame()
  convert_df_2_pkl()
  bert_w2v_mapper()
  finally_concat_pickles()
  create_vectors_text_meta_voice_with_predictions.create_labels_df_from_vectors()
  return

if __name__ == "__main__":
    main()

