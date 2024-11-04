from time import time
from logging import getLogger
from warnings import simplefilter

from scipy.cluster.hierarchy import linkage, ClusterWarning
from sklearn.metrics.pairwise import cosine_distances
from numpy import array

simplefilter("ignore", ClusterWarning)

logger = getLogger("similarity_calculator")


class AbstractSimilarityCalculator:

    def calculate_abstract_similarity(self, embedded_abstracts: array) -> array:

        initial_time = time()

        logger.info("Starting to cluster abstracts")

        distances_matrix = cosine_distances(embedded_abstracts)
        abstracts_similarity = linkage(
            distances_matrix, method="weighted", metric="cosine"
        )

        finish_time = time() - initial_time
        logger.info(f"Time to cluster abstracts: {finish_time}")

        logger.info("Clustered abstracts successfully")

        return abstracts_similarity
