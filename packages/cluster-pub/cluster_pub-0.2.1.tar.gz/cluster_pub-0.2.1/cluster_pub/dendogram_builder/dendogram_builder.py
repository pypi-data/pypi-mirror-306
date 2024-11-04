from typing import Dict
from time import time
from logging import getLogger

from matplotlib import pyplot
from matplotlib.style import use
from scipy.cluster.hierarchy import dendrogram
from numpy import array

logger = getLogger(__name__)


class DendogramBuilder:

    def build_dendogram_and_save(
        self, similarity_matrix: array, dendogram_labels: array, result_file: str
    ) -> None:

        initial_time = time()

        logger.info("Starting to generate dendogram")

        use(style="fast")

        self.build_dendogram(
            similarity_matrix=similarity_matrix,
            dendogram_labels=dendogram_labels,
            to_plot=True,
        )

        pyplot.subplots_adjust(top=30)
        pyplot.savefig(result_file, bbox_inches="tight")

        finish_time = time() - initial_time
        logger.info(f"Time to generate dendogram: {finish_time}")

        logger.info("Generated dendogram successfully")

    def build_dendogram(
        self, similarity_matrix: array, dendogram_labels: array, to_plot: bool = False
    ) -> Dict:

        initial_time = time()

        logger.info("Starting to calculate dendogram coordinates")

        no_plot = not to_plot

        built_dendogram = dendrogram(
            similarity_matrix,
            orientation="right",
            labels=dendogram_labels,
            no_plot=no_plot,
            leaf_font_size=10,
            show_contracted=True,
        )

        finish_time = time() - initial_time
        logger.info(f"Time to build dendogram coordinates: {finish_time}")

        logger.info("Dendogram coordinates built successfully")

        return built_dendogram
