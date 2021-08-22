import pandas as pd

speakers_dict = {}


def get_error_rate(path_to_pkl_with_speakers, path_to_pkl_with_clusters):
    true_positive_rate = 0
    source_df = pd.read_pickle(path_to_pkl_with_speakers)
    final_df = pd.read_pickle(path_to_pkl_with_clusters)

    start_row = 0
    end_row = 0

    for index, row in enumerate(final_df[['From', 'To', 'cluster']].to_numpy()):
        row_indexes = source_df.index[source_df['From'].between(row[0] - 0.01, row[1] + 0.01)]
        if(len(row_indexes) >= 2):
            start_row = row_indexes.values[0]
            end_row = row_indexes.values[len(row_indexes)-1]
        elif(len(row_indexes) == 1):
            start_row = row_indexes.values[0]
            end_row = row_indexes.values[0]
        else:
            print('no match for index ', index)
            print('start time: {}; end time: {}\n'.format(row[0], row[1]))

        #print("times & indexes")
        #print(row[0], row[1], start_row, end_row)
        for row_id in range(start_row, end_row):
                true_positive_rate += check_speaker(row_id, row, source_df)
            # For row with end time
        true_positive_rate += check_speaker(end_row, row, source_df)
    print("true_positive_rate {}, total {}".format(true_positive_rate, len(source_df)))
    return (1 - true_positive_rate / len(source_df)) * 100


def check_speaker(row_id, row, source_df):
    #print(speakers_dict)
    speaker_name = source_df._get_value(row_id, 'Speaker')
    speaker_from_dict = speakers_dict.get(row[2])

    if speaker_from_dict and speaker_name == speaker_from_dict:
        return 1
    else:
        if speaker_exists(speaker_name) == False:
            speakers_dict[row[2]] = speaker_name
            #print('speakers_dict', speakers_dict)
            return 1
    return 0


def speaker_exists(speaker_name):
    for value in speakers_dict.values():
        if speaker_name == value:
            return True
    return False
