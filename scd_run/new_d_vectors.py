'''
    New d-vectors creation & comparison
    Rows taken from create_vectors_text_meta_voice.py file
    by Olga & Ron

'''

'''
    Do we get pickle or dir?
    How data labeled as SC?
'''
    def run_scd(pickle):
        '''
        For each sc in pickle:
 	        If sc.label: (data_df[data_df["Label"] == "Changed"] ) (Note:  data_df = pd.read_pickle(PATH + "Pickles/raw_data_2_convert_2_embeddings.pkl") row 236)
                (Note: Check first & last two records even if change not detected!!!!! )

                For each record in sc: (~O1)
                    Create d-vectors & save them to temp_pickle
                    (Note func: row 128 -> create_vectors(df, w2v))
                End for

                For each sample in pickle:
	                Check vector similarity with next one:
                        Label them by start & end time of speech of the same speaker
				        (Note: save end time of this vector as start of next!!)
				        (Note: ( row 192)
				                vectors_pkl.iloc[i][meta_data_start_index + 1] = df.iloc[i]["Start_Time"]
                                vectors_pkl.iloc[i][meta_data_start_index + 2] = df.iloc[i]["End_Time"]
                                vectors_pkl.iloc[i][meta_data_start_index + 3] = df.iloc[i]["ID?"])
                end for

                save labeled pickle as new_pickle (row 243)
        end for

        '''
        return new_pickle
