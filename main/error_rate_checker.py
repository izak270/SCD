import pandas as pd
import settings

settings.init()
def get_error_rate():
    source_df = pd.read_pickle(settings.PATH + 'Pickles/Bmr020_with_labels.pkl')
    final_df = pd.read_pickle(settings.PATH + 'Pickles/vec/pkl_with_clusters.pkl')
    print(source_df)
    print(final_df)
    speakers_dict = {}
    true_positive_rate = 0
    for row in final_df:
        print(row)
        start_row = source_df.loc[(source_df['From'] == row['start'])]
        end_row = source_df.loc[(source_df['To'] == row['finish'])]
        for word in range(start_row, end_row):
            # Speaker in already in dict
            speaker_id = speakers_dict.get(source_df.loc[(source_df['Speaker'])])
            if speaker_id:
                if speaker_id == row['cluster']:
                    true_positive_rate += 1
            else:
                speakers_dict[source_df.loc[(source_df['Speaker'])]] = speaker_id
                true_positive_rate += 1

    return true_positive_rate / len(source_df)

