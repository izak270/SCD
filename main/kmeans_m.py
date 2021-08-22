import xlsxwriter
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from kneed import KneeLocator
import math
import settings
from error_rate_checker import get_error_rate



settings.init()
def kmeans():
    df = pd.read_pickle(settings.PATH + 'Pickles/vec/prepared_vectors_2_split-RON_OLGA.pkl')
    df.head()
    my_list = [i for i in range(256)]
    df2 = df[df['Vectors'].notna()]
    start = pd.DataFrame(df2['From'].to_list(), columns=['From'])
    finish = pd.DataFrame(df2['To'].to_list(), columns=['To'])
    gf3 = pd.DataFrame(df2['Vectors'].to_list(), columns=my_list)
    gf3 = gf3[gf3[0].notna()]
    sse = []

    print("Data frame length: " + str(len(gf3)))

    if len(gf3) > 50:  
      k_rng = range(1, 50)
    else:
      k_rng = range(1, len(gf3))

    for k in k_rng:
        print(k)
        km = KMeans(n_clusters=k)
        km.fit(gf3[my_list])
        sse.append(km.inertia_)

    x = range(1, len(k_rng)+1)
    kn = KneeLocator(x, sse, curve='convex', direction='decreasing')
    print("Number of clusters: " + str(kn.knee))

    km = KMeans(n_clusters=kn.knee)
    y_predicted = km.fit_predict(gf3[my_list])
    print(y_predicted,'yy')
    gf3['cluster']=y_predicted
    gf3['From']=start
    gf3['To']=finish
    pd.to_pickle(gf3, settings.PATH + "Pickles/vec/pkl_with_clusters.pkl")
    fileName = settings.PATH + "Excels/Data_Frame_With_Labels_And_Clusters.xlsx"
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.set_column(0, 3, 15)

    worksheet.write(0, 0, "cluster", bold)
    worksheet.write(0, 1, "Start Time", bold)
    worksheet.write(0, 2, "End Time", bold)

    # plt.xlabel('K')
    # plt.ylabel('Sum of squared error')
    # plt.plot(k_rng, sse)
    # plt.show()
    for k in range(0, len(gf3)):
        worksheet.write((k + 1), 0, gf3.iloc[k]['cluster'])
        worksheet.write((k + 1), 1, gf3.iloc[k]['From'])
        worksheet.write((k + 1), 2, gf3.iloc[k]['To'])
    workbook.close()
    return gf3

def start():
    kmeans()
    general_df = pd.read_pickle(settings.PATH + "Pickles/general_df_4_all_files.pkl")
    file_name = general_df["ID"].iloc[0]
    error = get_error_rate(settings.PATH + "Pickles/" + file_name + "_with_labels.pkl" , settings.PATH + "Pickles/vec/pkl_with_clusters.pkl")
    print('ERROR: ', error, '%')
  