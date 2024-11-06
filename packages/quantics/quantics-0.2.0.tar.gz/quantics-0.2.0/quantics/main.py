import umap
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class QUANTICS:
    def __init__(self, dataset):
        if isinstance(dataset, (np.ndarray, pd.DataFrame)):
            self.dataset = dataset
        else:
            raise ValueError("Dataset must be a numpy array or pandas dataframe")
        self.scaler_model = None
        self.normalized_data = None
        self.reduction_model = None
        self.reduced_data = None
        self.cluster_model = None
    
    def normalize(self, normalize_method='z-score', **args):
        normalize_method = normalize_method.lower()
        if normalize_method == 'z-score':
            self.scaler_model = StandardScaler(**args)
        elif normalize_method == 'minmax':
            self.scaler_model = MinMaxScaler(**args)
        else:
            raise ValueError("normalize_method must be 'z-score' or 'minmax'")
        
        self.normalized_data = self.scaler_model.fit_transform(self.dataset)
        
    
    def reduce_dim(self, data, reduction_method='umap', dim_size=2, **args):
        reduction_method = reduction_method.lower()
        if reduction_method == 'pca':
            self.reduction_model = PCA(n_components=dim_size, **args)
        elif reduction_method == 'tsne':
            self.reduction_model = TSNE(n_components=dim_size, **args)
        elif reduction_method == 'umap':
            self.reduction_model = umap.UMAP(n_components=dim_size, **args)
        else:
            raise ValueError("reduction_method must be 'pca', 'tsne', or 'umap'")
        
        self.reduced_data = self.reduction_model.fit_transform(data)
       

    def cluster(self, min_k=2, max_k=36, **args):
        if self.reduced_data is None:
            raise ValueError("Reduced data not found. Perform dimensionality reduction before clustering.")
        
        best_k = min_k
        best_score = -1
        best_model = None
        
        for k in range(min_k, max_k + 1):
            model = KMeans(n_clusters=k,n_init='auto', **args)
            labels = model.fit_predict(self.reduced_data)
            score = silhouette_score(self.reduced_data, labels)
            if score > best_score:
                best_k = k
                best_score = score
                best_model = model
        
        self.cluster_model = best_model
        print(f"Optimal K: {best_k}, Silhouette Score: {best_score}")
    
    def get_representative_samples(self, no_samples=5):
        """
        Extracts representative samples based on the clustered data.

        Args:
            no_samples: Number of representative samples to extract.

        Raises:
            ValueError: If no clustering model has been fit.
        """
        if self.cluster_model is None:
            raise ValueError("No clustering model found. Run clustering first.")

        labels = self.cluster_model.labels_
        unique_labels = np.unique(labels)
        all_representative_indices = []

        if len(unique_labels) > no_samples:
            # More clusters than desired samples: Randomly select clusters
            selected_clusters = np.random.choice(unique_labels, no_samples, replace=False)

            for cluster_id in selected_clusters:
                cluster_mask = labels == cluster_id
                cluster_distances = self.cluster_model.transform(self.reduced_data[cluster_mask])[:, 0]
                closest_index = np.argmin(cluster_distances)
                all_representative_indices.append(np.flatnonzero(cluster_mask)[closest_index])
        else:
            # Fewer clusters than desired samples: Get closest from all clusters, then farthest from some
            for cluster_id in unique_labels:
                cluster_mask = labels == cluster_id
                cluster_distances = self.cluster_model.transform(self.reduced_data[cluster_mask])[:, 0]
                closest_index = np.argmin(cluster_distances)
                all_representative_indices.append(np.flatnonzero(cluster_mask)[closest_index])

            remaining_samples = no_samples - len(unique_labels)
            remaining_clusters = np.random.choice(unique_labels, remaining_samples, replace=True)  # Allow replacement for potentially small datasets

            for cluster_id in remaining_clusters:
                cluster_mask = labels == cluster_id
                cluster_distances = self.cluster_model.transform(self.reduced_data[cluster_mask])[:, 0]
                farthest_index = np.argmax(cluster_distances)
                all_representative_indices.append(np.flatnonzero(cluster_mask)[farthest_index])

        return self.dataset.iloc[all_representative_indices] if isinstance(self.dataset, pd.DataFrame) else self.dataset[all_representative_indices]