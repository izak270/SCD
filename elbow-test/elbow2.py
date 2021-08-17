from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
from kneed import KneeLocator

iris = load_iris()

df = pd.DataFrame(iris.data,columns=iris.feature_names)
df.head()
print(df,'!@!@@12')
# plt.scatter(df/)
df['flower'] = iris.target
df.head()

df.drop(['sepal length (cm)', 'sepal width (cm)', 'flower'],axis='columns',inplace=True)
df.head(3)

km = KMeans(n_clusters=3)
yp = km.fit_predict(df)
yp

df['cluster'] = yp
df.head(2)

df.cluster.unique()


df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster==2]


plt.scatter(df1['petal length (cm)'],df1['petal width (cm)'],color='blue')
plt.scatter(df2['petal length (cm)'],df2['petal width (cm)'],color='green')
plt.scatter(df3['petal length (cm)'],df3['petal width (cm)'],color='yellow')

sse = []
k_rng = range(1,10)
for k in k_rng:
    km = KMeans(n_clusters=k)
    km.fit(df)
    print(df)
    sse.append(km.inertia_)
x = range(1, len(k_rng)+1)


kn = KneeLocator(x, sse, curve='convex', direction='decreasing')
print(kn.knee)
plt.xlabel('K')
plt.ylabel('Sum of squared error')
plt.plot(k_rng, sse)
plt.show()

