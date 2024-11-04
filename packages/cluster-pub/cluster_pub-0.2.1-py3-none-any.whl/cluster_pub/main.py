import logging
from typing_extensions import Annotated

from typer import Typer, Argument, Option
from rich.progress import Progress, SpinnerColumn, TextColumn

from cluster_pub.cluster_publications import ClusterPub

application = Typer()


@application.command()
def cluster_publications(
    source_file: Annotated[
        str,
        Argument(
            help="Path for Bibliography File. Allowed Bibliographic File Extensions:"
            " BibTex (.bib), RIS (.ris) and NBIB (.nbib)"
        ),
    ],
    result_file: Annotated[
        str,
        Argument(
            help="Path to store result file. Allowed File extensions:"
            " EPS, JPEG, JPG, PDF, PGF, PNG, PS, Raw, RGBA, SVG, SVGZ, TIF, TIFF, Webp"
        ),
    ],
    verbose: Annotated[
        bool, Option(help="Flag to enable displaying logging messages")
    ] = False,
):

    if verbose:
        logging.basicConfig(level=logging.INFO)

    cluster_pub_instance = ClusterPub()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress_manager:

        cluster_pub_instance.cluster_publications(
            source_bibliography_file=source_file,
            result_file=result_file,
            progress_manager=progress_manager,
        )

        progress_manager.print("[green]Publications clustered successfully ✓ ")


if __name__ == "__main__":
    application()
