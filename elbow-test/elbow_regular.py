
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_pickle("vector_olga_ron.pkl")
print(df)

scaler = MinMaxScaler()
# print(df[[2]],'ghj')
print(type(df[[2]]))
x1 = np.array(df[[2]])
print('x11111111111111',x1[12])
X = np.array([[1, 2], [1, 4], [1, 0],
               [4, 2], [4, 4], [4, 0]])
print('@!!@!@',X)
print(type(X))

# print(x1)
# print('!!!!',X)
kmeans = KMeans(n_clusters=2).fit(x1)
# print(kmeans)
# scaler.fit(df[[2]])
#
# df['Income($)'] = scaler.transform(df[['Income($)']])
#
# scaler.fit(df[['Age']])
# df['Age'] = scaler.transform(df[['Age']])
#
# df.head()
#
# # plt.scatter(df.Age,df['Income($)'])
#
#
#
# sse = []
# k_rng = range(1, 10)
#
# for k in k_rng:
#     km = KMeans(n_clusters=k)
#     print(km)
#     km.fit(df[['Age', 'Income($)']])
#     sse.append(km.inertia_)
# x = range(1, len(k_rng)+1)
#
#
# kn = KneeLocator(x, sse, curve='convex', direction='decreasing')
# print(kn.knee)
#
# km = KMeans(n_clusters=kn.knee)
# y_predicted = km.fit_predict(df[['Age','Income($)']])
# y_predicted
# print(y_predicted,'ypredi')
# df['cluster']=y_predicted
# df.head()
#
# km.cluster_centers_
#
# df1 = df[df.cluster==0]
# df2 = df[df.cluster==1]
# df3 = df[df.cluster==2]
# plt.scatter(df1.Age,df1['Income($)'],color='green')
# plt.scatter(df2.Age,df2['Income($)'],color='red')
# plt.scatter(df3.Age,df3['Income($)'],color='black')
# plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')
# plt.legend()
# plt.show()
# print(sse)
# plt.xlabel('K')
# plt.ylabel('Sum of squared error')
# plt.plot(k_rng,sse)
# plt.show()
#


