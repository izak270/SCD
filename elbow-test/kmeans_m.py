
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from kneed import KneeLocator
import math

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
print(y_predicted)
print(len(y_predicted))
gf3['cluster']=y_predicted
gf3['start']=start
gf3['finish']=finish
print(gf3,'ypredi')


