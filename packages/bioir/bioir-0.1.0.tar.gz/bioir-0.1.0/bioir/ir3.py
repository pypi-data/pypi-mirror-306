
print("""from sklearn.datasets import load_iris
from sklearn.decomposition import PCA

from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram,linkage

iris = load_iris()
X = iris.data

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)
X_scaled[:2]

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)
X_pca[:2]


Z = linkage(X_pca,'ward')
plt.figure(figsize=(10,6))
dendrogram(Z)
plt.show()

clustering = AgglomerativeClustering(n_clusters=3)
clustering.fit(X_pca)

plt.scatter(X_pca[:,0],X_pca[:,1],c=clustering.labels_,cmap='rainbow')""")

