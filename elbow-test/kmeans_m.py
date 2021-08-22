import xlsxwriter
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from kneed import KneeLocator
import math
PATH = "/home/itzhak/SCD/"
df = pd.read_pickle('vector_olga_ron.pkl')
print(df)
df.head()
my_list = [i for i in range(256)]

df2 = df[df[2].notna()]
print('df2',df2)
start = pd.DataFrame(df2[0].to_list(), columns=['start'])
finish = pd.DataFrame(df2[1].to_list(), columns=['finish'])
print('startf',start)
print('startf',finish)
gf3 = pd.DataFrame(df2[2].to_list(), columns=my_list)
print('gf3',gf3)
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
print(y_predicted,'ypredict')
print(len(y_predicted))
gf3['cluster']=y_predicted
gf3['start']=start
gf3['finish']=finish
print(gf3,'ypredi')

fileName = PATH + "main/xlsx/Data_Frame_WithLabels7.xlsx"
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.set_column(0, 3, 15)

worksheet.write(0, 0, "cluster", bold)
worksheet.write(0, 1, "Start Time", bold)
worksheet.write(0, 2, "End Time", bold)

plt.xlabel('K')
plt.ylabel('Sum of squared error')
plt.plot(k_rng,sse)
plt.show()

for k in range(0, len(gf3)):
    worksheet.write((k + 1), 0, gf3.iloc[k]['cluster'])
    worksheet.write((k + 1), 1, gf3.iloc[k]['start'])
    worksheet.write((k + 1), 2, gf3.iloc[k]['finish'])
    # for j in range(0, 3):
    #     size = len(gf3.columns)+j-3
    #     print(size,'len')
    #     print(gf3.iloc[k][size],'test')
    #     worksheet.write((k + 1), j, gf3.iloc[k][len(gf3.columns)+j-6])

workbook.close()
