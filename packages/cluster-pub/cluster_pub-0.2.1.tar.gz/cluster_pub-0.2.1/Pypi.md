# ClusterPub

ClusterPub is a tool developed to help researchers in their processes of bibliographic review, 
helping them to find papers related to their areas of interest,
based on search results returned by papers repositories, like, IEEE Xplore and Pubmed.

## Instalation 🛠

To install and execute ClusterPub it is necessary to have Python 3.11 or above installed.

## Run ClusterPub 🚀

To execute ClusterPub run the following command:

#### Cluster publications present in a bibliographic file
```bash Python installation command
cluster-pub {source_file} {result_file}
```

#### OBS: The result_file name should contain the desired extension.

The allowed extensions for the source file are:

- NBIB
- RIS
- BibTex

The allowed extensions for the result file are:

- EPS
- JPEG
- PDF
- PGF
- PNG
- PS
- Raw (Binary)
- RGBA
- SVG
- SVGZ
- TIF
- TIFF
- Webp


#### To obtain help about the parameters and options available execute the following command:
```bash Python installation command
cluster-pub --help
```

There is a folder in the project directory called sample_files, containing files that could be used to execute tests.

## Extract Clustering Metrics  📈

To calculate clustering metrics, like, Silhouette Score, Davies-Bouldin Score and Calinski-Harabasz Score run the following commands:

OBS: The argument number_of_clusters is not the desired clusters quantity,
but it is the quantity of clusters/categories that might exit in the analysed dataset.

#### Calculate Davies-Bouldin Score
```bash Python installation command
cluster-pub-metrics davies-bouldin-score {source_file} {number_of_clusters}
```

#### Calculate Calinski-Harabasz Score
```bash Python installation command
cluster-pub-metrics calinski-harabasz-score {source_file} {number_of_clusters}
```

#### Calculate Silhouette Score
```bash Python installation command
cluster-pub-metrics silhouette-score {source_file} {number_of_clusters} --distance-metric={distance_metric}
```

#### To obtain help for the score commands listed above run the following command:
```bash Python installation command
cluster-pub-metrics {score_command} -- help
```

## Background Information 🔍

The default hyperparameters and algorithms used in this project are:

- Word Embeddings Technicque: Hash2Vec
- Dimensionality Reduction Technicque: SVD
- Number of singular values used in SVD: 8
- Clustering Algorithm: Hierarchical Clustering
- Distance Metric: Cosine Similarity
- Linkage Method: Weighted
- Supported Languages: English