import pandas as pd
from time import gmtime, strftime

PATH = "/home/user/IdeaProjects/libonea/demos/SCD/ICSI_Dataset/"

df = pd.read_pickle(PATH + "Pickles/general_df_4_all_files.pkl")

id_list = sorted(list(set(df["ID"])))

data_to_convert_df = pd.DataFrame(columns=['ID', 'First_Word', 'Second_Word', 'Third_Word',
                                           'Fourth_Word', 'Fifth_Word', 'Sixth_Word',
                                           'First_Duration', 'Second_Duration', 'Third_Duration',
                                           'Fourth_Duration', 'Fifth_Duration', 'Sixth_Duration',
                                           'First_Normal', 'Second_Normal', 'Third_Normal',
                                           'Fourth_Normal', 'Fifth_Normal', 'Sixth_Normal',
                                           'Segment_Start', 'Segment_Middle_1', 'Segment_Middle_2', 'Segment_End',
                                           'Space_3_4', 'Label'])
cntr = 0

for id in id_list:
    df_for_id = df[df["ID"] == id]

    for i in range(len(df_for_id) - 6):
        sub_df = df_for_id[i:i + 6]

        first_word = str(sub_df.iloc[0]["Word"])
        first_duration = float(sub_df.iloc[0]["To"]) - float(sub_df.iloc[0]["From"])
        first_normal = first_duration / len(first_word)

        second_word = str(sub_df.iloc[1]["Word"])
        second_duration = float(sub_df.iloc[1]["To"]) - float(sub_df.iloc[1]["From"])
        second_normal = second_duration / len(second_word)

        third_word = str(sub_df.iloc[2]["Word"])
        third_duration = float(sub_df.iloc[2]["To"]) - float(sub_df.iloc[2]["From"])
        third_normal = third_duration / len(third_word)

        fourth_word = str(sub_df.iloc[3]["Word"])
        fourth_duration = float(sub_df.iloc[3]["To"]) - float(sub_df.iloc[3]["From"])
        fourth_normal = fourth_duration / len(fourth_word)

        fifth_word = str(sub_df.iloc[4]["Word"])
        fifth_duration = float(sub_df.iloc[4]["To"]) - float(sub_df.iloc[4]["From"])
        fifth_normal = fifth_duration / len(fifth_word)

        sixth_word = str(sub_df.iloc[5]["Word"])
        sixth_duration = float(sub_df.iloc[5]["To"]) - float(sub_df.iloc[5]["From"])
        sixth_normal = sixth_duration / len(sixth_word)

        segment_start = sub_df.iloc[0]["From"]
        segment_middle_1 = sub_df.iloc[2]["To"]
        segment_middle_2 = sub_df.iloc[3]["From"]
        segment_end = sub_df.iloc[5]["To"]

        space_3_4 = float(sub_df.iloc[3]["From"]) - float(sub_df.iloc[2]["To"])

        label = "Same"
        if str(sub_df.iloc[2]["Speaker"]) != str(sub_df.iloc[3]["Speaker"]):
            label = "Split"

        example_df = pd.DataFrame([[id, first_word, second_word, third_word, fourth_word, fifth_word, sixth_word,
                                    first_duration, second_duration, third_duration,
                                    fourth_duration, fifth_duration, sixth_duration,
                                    first_normal, second_normal, third_normal,
                                    fourth_normal, fifth_normal, sixth_normal,
                                    segment_start, segment_middle_1, segment_middle_2, segment_end,
                                    space_3_4, label]],
                                  columns=data_to_convert_df.columns.values)

        data_to_convert_df = data_to_convert_df.append(example_df)

    cntr += 1
    print(str(cntr) + " Out of: " + str(len(id_list)) + "    " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))

    if 0 == cntr % 10:
        pd.to_pickle(data_to_convert_df, PATH + "Pickles/Concat/" + str(cntr) + "-data_to_convert_df_speech_text_hybrid.pkl")

        data_to_convert_df = pd.DataFrame(columns=['ID', 'First_Word', 'Second_Word', 'Third_Word',
                                           'Fourth_Word', 'Fifth_Word', 'Sixth_Word',
                                           'First_Duration', 'Second_Duration', 'Third_Duration',
                                           'Fourth_Duration', 'Fifth_Duration', 'Sixth_Duration',
                                           'First_Normal', 'Second_Normal', 'Third_Normal',
                                           'Fourth_Normal', 'Fifth_Normal', 'Sixth_Normal',
                                           'Segment_Start', 'Segment_Middle_1', 'Segment_Middle_2', 'Segment_End',
                                           'Space_3_4', 'Label'])

pd.to_pickle(data_to_convert_df, PATH + "Pickles/Concat/" + "last_data_to_convert_df_speech_text_hybrid.pkl")

pass
