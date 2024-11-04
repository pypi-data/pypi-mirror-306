from functools import partial

from numpy import array
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score,
)

from cluster_pub.bibliography_parsers.bibliography_parser import BibliographyParser
from cluster_pub.bibliography_abstract_processor.bibliography_abstract_processor import (
    BibliographyAbstractProcessor,
)
from cluster_pub.abstract_embedder.abstract_embedder import AbstractEmbedder
from cluster_pub.abstract_similarity_calculator.abstract_similarity_calculator import (
    AbstractSimilarityCalculator,
)

cosine_silhouette_score_function = partial(silhouette_score, metric="cosine")


class ClusteringEvaluator:

    _clusters_scores_functions = {
        "silhouette_score_euclidean": silhouette_score,
        "silhouette_score_cosine": cosine_silhouette_score_function,
        "calinski_harabasz_score": calinski_harabasz_score,
        "davies_bouldin_score": davies_bouldin_score,
    }

    def __init__(self):
        self.bibliography_parser = BibliographyParser()
        self.bibliography_processor = BibliographyAbstractProcessor()
        self.abstract_embedder = AbstractEmbedder()
        self.similarity_calculator = AbstractSimilarityCalculator()
        self.number_of_repetitions = 10

    def calculate_clusters_silhouette_score(
        self,
        bibliography_file: str,
        number_of_clusters: int,
        distance_metric: str = "euclidean",
    ) -> float:

        silhouette_score_function = f"silhouette_score_{distance_metric}"

        clusters_silhouette_scores = list(
            self.calculate_clusters_score(
                bibliography_file=bibliography_file,
                number_of_clusters=number_of_clusters,
                clusters_score=silhouette_score_function,
            )
            for _ in range(self.number_of_repetitions)
        )
        clusters_silhouette_score = sum(clusters_silhouette_scores) / len(
            clusters_silhouette_scores
        )

        return clusters_silhouette_score

    def calculate_clusters_davies_bouldin_score(
        self, bibliography_file: str, number_of_clusters: int
    ) -> float:

        clusters_davies_bouldin_scores = list(
            self.calculate_clusters_score(
                bibliography_file=bibliography_file,
                number_of_clusters=number_of_clusters,
                clusters_score="davies_bouldin_score",
            )
            for _ in range(self.number_of_repetitions)
        )
        clusters_davies_bouldin_score = sum(clusters_davies_bouldin_scores) / len(
            clusters_davies_bouldin_scores
        )

        return clusters_davies_bouldin_score

    def calculate_clusters_calinski_harabasz_score(
        self, bibliography_file: str, number_of_clusters: int
    ) -> float:

        clusters_calinski_harabasz_scores = list(
            self.calculate_clusters_score(
                bibliography_file=bibliography_file,
                number_of_clusters=number_of_clusters,
                clusters_score="calinski_harabasz_score",
            )
            for _ in range(self.number_of_repetitions)
        )
        clusters_calinski_harabasz_score = sum(clusters_calinski_harabasz_scores) / len(
            clusters_calinski_harabasz_scores
        )

        return clusters_calinski_harabasz_score

    def calculate_clusters_score(
        self, bibliography_file: str, number_of_clusters: int, clusters_score: str
    ) -> float:

        embedded_abstracts = self.embed_bibliography_abstracts(
            bibliography_file=bibliography_file
        )

        abstracts_clusters = self.similarity_calculator.calculate_abstract_similarity(
            embedded_abstracts=embedded_abstracts
        )

        abstracts_clusters_labels = self.get_clusters_labels(
            clusters=abstracts_clusters, number_of_clusters=number_of_clusters
        )

        clusters_score_function = self._clusters_scores_functions.get(clusters_score)

        clusters_index_score = clusters_score_function(
            embedded_abstracts, labels=abstracts_clusters_labels
        )

        return clusters_index_score

    def embed_bibliography_abstracts(self, bibliography_file: str) -> array:

        parsed_bibliography_file_entries = (
            self.bibliography_parser.parse_bibliography_file(
                bibliography_file=bibliography_file
            )
        )

        processed_bibliography_file_entries = (
            self.bibliography_processor.process_bibliography_file_entries(
                bibliography_file_entries=parsed_bibliography_file_entries
            )
        )

        embedded_bibliography_abstracts = (
            self.abstract_embedder.embed_bibliography_abstracts(
                bibliography_abstracts=processed_bibliography_file_entries
            )
        )

        return embedded_bibliography_abstracts

    def get_clusters_labels(self, clusters: array, number_of_clusters: int) -> array:

        clusters_labels = fcluster(clusters, t=number_of_clusters, criterion="maxclust")

        return clusters_labels
