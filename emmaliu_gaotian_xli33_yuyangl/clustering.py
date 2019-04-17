
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.datasets.samples_generator import make_blobs
X, y_true = make_blobs(n_samples=200, centers=3, cluster_std=0.60, random_state=0)
plt.scatter(X[:,0],X[:,1],s=50) 

from sklearn.cluster import KMeans
kmeans=Kmeans(n_clusters=3)
kmeans.fit(X)
y_kmeans=kmeans.predict(X)

from sklearn.metrics import pairwise_distances_argmin

def find_clusters(X, n_clusters, rseed=2):
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = x[i]

    while True:
        labels = pairwise_distances_argmin(X,centers)
        new_centers=np.array([X[labels == i].mean(0) for i in range(n_clusters)])

        if np.all(centers == new_centers):
            break
        centers = new_centers

    return centers, labels

plt.scatter(X[:,0],X[:,1],c=y_kmeans,s=50,cmap='viridis')
plt.scatter(centers[:,0],centers[:,1],c='black',s=200,alpha=0.5);


data = pd.read_csv('tweets_amman.csv')
print(data.shape)
data.dead()


