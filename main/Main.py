from pre_process_utils import convert_origin_2_raw_data, convert_raw_data_2_data_frame, convert_df_2_pkl, \
  bert_w2v_mapper, finally_concat_pickles


def main():
  # convert_origin_2_raw_data()
  # convert_raw_data_2_data_frame()
  # convert_df_2_pkl()
  bert_w2v_mapper()
  finally_concat_pickles()
  return

if __name__ == "__main__":
    main()

