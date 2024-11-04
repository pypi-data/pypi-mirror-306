from typing import List
from time import time
from logging import getLogger

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.decomposition import TruncatedSVD
from numpy import array


from ..bibliography_abstract_processor.schemas import ProcessedBibliographyFileData

logger = getLogger(__name__)


class AbstractEmbedder:

    def __init__(self):
        self.abstract_vectorizer = HashingVectorizer(
            analyzer="char", ngram_range=(4, 5)
        )
        self.dimensionality_reducer = TruncatedSVD(n_components=8)

    def embed_bibliography_abstracts(
        self, bibliography_abstracts: List[ProcessedBibliographyFileData]
    ) -> array:

        initial_time = time()

        logger.info("Starting to embed abstracts")

        abstracts_to_embed = array(
            [
                bibliography_abstract["processed_abstract"]
                for bibliography_abstract in bibliography_abstracts
            ],
            dtype=str,
        )

        embedded_abstracts_matrix = self.abstract_vectorizer.fit_transform(
            abstracts_to_embed
        )

        reduced_embedded_abstracts_matrix = self.dimensionality_reducer.fit_transform(
            embedded_abstracts_matrix
        )

        finish_time = time() - initial_time
        logger.info(f"Time to embed abstracts: {finish_time}")

        logger.info("Embedded abstracts successfully")

        return reduced_embedded_abstracts_matrix
