from typing_extensions import Annotated

from typer import Typer, Argument, Option
from rich import print

from cluster_pub.clustering_evaluator import ClusteringEvaluator

clustering_evaluator_instance = ClusteringEvaluator()

application = Typer()


@application.command(name="davies-bouldin-score")
def calculate_davies_bouldin_score(
    source_file: Annotated[
        str,
        Argument(
            help="Path for Bibliography File. Allowed Bibliographic File Extensions: "
            "BibTex (.bib), RIS (.ris) and NBIB (.nbib)"
        ),
    ],
    number_of_clusters: Annotated[
        int, Argument(help="Quantity of Categories/Clusters present in the source file")
    ],
):

    davies_bouldin_score = (
        clustering_evaluator_instance.calculate_clusters_davies_bouldin_score(
            bibliography_file=source_file, number_of_clusters=number_of_clusters
        )
    )

    print(f"Davies-Bouldin Score: {davies_bouldin_score}")


@application.command(name="calinski-harabasz-score")
def calculate_calinski_harabasz_score(
    source_file: Annotated[
        str,
        Argument(
            help="Path for Bibliography File. Allowed Bibliographic File Extensions:"
            " BibTex (.bib), RIS (.ris) and NBIB (.nbib)"
        ),
    ],
    number_of_clusters: Annotated[
        int, Argument(help="Quantity of Categories/Clusters present in the source file")
    ],
):

    calinski_harabasz_score = (
        clustering_evaluator_instance.calculate_clusters_calinski_harabasz_score(
            bibliography_file=source_file, number_of_clusters=number_of_clusters
        )
    )

    print(f"Calinski-Harabasz Score: {calinski_harabasz_score}")


@application.command(name="silhouette-score")
def calculate_silhouette_score(
    source_file: Annotated[
        str,
        Argument(
            help="Path for Bibliography File. Allowed Bibliographic File Extensions:"
            " BibTex (.bib), RIS (.ris) and NBIB (.nbib)"
        ),
    ],
    number_of_clusters: Annotated[
        int, Argument(help="Quantity of Categories/Clusters present in the source file")
    ],
    distance_metric: Annotated[
        str,
        Option(
            help="Distance Metric to be used during evaluation. Allowed Distance Metrics: euclidean and cosine"
        ),
    ] = "euclidean",
):

    silhouette_score = (
        clustering_evaluator_instance.calculate_clusters_silhouette_score(
            bibliography_file=source_file,
            number_of_clusters=number_of_clusters,
            distance_metric=distance_metric,
        )
    )

    print(f"Silhouette Score: {silhouette_score}")


if __name__ == "__main__":
    application()
