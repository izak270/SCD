from sklearn.cluster import KMeans
import pandas as pd
from kneed import KneeLocator
from error_rate_checker import get_error_rate

PATH = "../Pickles/"
PICKLE_WITH_VECTORS = 'vec/prepared_vectors_2_split-RON_OLGA.pkl'
FINALE_PICKLE_NAME = "clusters"
#TODO: put here path
PICKLE_WITH_SPEAKERS_NAME = ""

def kmeans():
    df = pd.read_pickle(PATH + PICKLE_WITH_VECTORS)
    print(df)
    df.head()
    my_list = [i for i in range(256)]

    '''df2 = df[df['Vectors'].notna()]
    start = pd.DataFrame(df2['From'].to_list(), columns=['start'])
    finish = pd.DataFrame(df2['To'].to_list(), columns=['finish'])
    gf3 = pd.DataFrame(df2['Vectors'].to_list(), columns=my_list)
    gf3 = gf3[gf3[0].notna()]'''
    df2 = df[df[2].notna()]
    start = pd.DataFrame(df2[0].to_list(), columns=['start'])
    finish = pd.DataFrame(df2[1].to_list(), columns=['finish'])
    gf3 = pd.DataFrame(df2[2].to_list(), columns=my_list)
    gf3 = gf3[gf3[0].notna()]
    print(gf3)
    sse = []
    k_rng = range(1, len(gf3))

    for k in k_rng:
        km = KMeans(n_clusters=k)
        km.fit(gf3[my_list])
        sse.append(km.inertia_)

    x = range(1, len(k_rng)+1)
    kn = KneeLocator(x, sse, curve='convex', direction='decreasing')
    print(kn.knee)

    km = KMeans(n_clusters=kn.knee)
    y_predicted = km.fit_predict(gf3[my_list])
    y_predicted
    gf3['cluster']=y_predicted
    gf3['start']=start
    gf3['finish']=finish
    print(gf3)

    pd.to_pickle(gf3, PATH + FINALE_PICKLE_NAME + ".pkl")
    print('Pickle Saved')
    gf3.to_excel(PATH + FINALE_PICKLE_NAME + ".xlsx")
    print('XLSX Saved')


    # fileName = PATH + "main/Data_Frame_WithLabels2.xlsx"
    # workbook = xlsxwriter.Workbook(fileName)
    # worksheet = workbook.add_worksheet()
    # bold = workbook.add_format({'bold': True})
    # worksheet.set_column(0, 3, 15)
    #
    # worksheet.write(0, 0, "cluster", bold)
    # worksheet.write(0, 1, "Start Time", bold)
    # worksheet.write(0, 2, "End Time", bold)
    #
    # for k in range(0, len(gf3)):
    #     worksheet.write((k + 1), 0, gf3.iloc[k]['cluster'])
    #     worksheet.write((k + 1), 1, gf3.iloc[k]['start'])
    #     worksheet.write((k + 1), 2, gf3.iloc[k]['finish'])
    # workbook.close()

def startk():
        kmeans()
        #TODO: check if working (need speakers lable in pkl)
        #error = get_error_rate(PATH + PICKLE_WITH_SPEAKERS_NAME, PATH + FINALE_PICKLE_NAME)
        #print('ERROR: ', error, '%')
        return

startk()
