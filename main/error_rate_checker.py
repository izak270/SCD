import pandas as pd

speakers_dict = {}

def get_error_rate(path_to_pkl_with_speakers, path_to_pkl_with_clusters):
    true_positive_rate = 0
    source_df = pd.read_pickle(path_to_pkl_with_speakers)
    final_df = pd.read_pickle(path_to_pkl_with_clusters)

    for index, row in enumerate(final_df[['From', 'To', 'cluster']].to_numpy()):
        start_row = 0
        end_row = 0
        row_indexes = source_df.index[source_df['From'].between(row[0] - 0.01, row[1] + 0.01)]
        if(len(row_indexes) == 2):
            start_row, end_row = row_indexes.values
        elif(len(row_indexes) == 1):
            start_row = row_indexes.values[0]
            end_row = row_indexes.values[0]
        else:
             print('no match for index ', index)

        #print("times & indexes")
        #print(row[0], row[1], start_row, end_row)
        for row_id in range(start_row, end_row):
                true_positive_rate += check_speaker(row_id, row, source_df)
            # For row with end time
        true_positive_rate += check_speaker(row_id + 1, row, source_df)
    print("true_positive_rate {}, total {}".format(true_positive_rate, len(source_df)))
    return (1 - true_positive_rate / len(source_df)) * 100


def check_speaker(row_id, row, source_df):
    speaker_id = speakers_dict.get(source_df._get_value(row_id, 'Speaker'))
    if speaker_id:
        if speaker_id == row['cluster']:
            return 1
    else:
        speakers_dict[source_df._get_value(row_id, 'Speaker')] = speaker_id
        return 1
    return 0
