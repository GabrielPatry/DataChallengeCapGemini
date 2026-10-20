"""DataChallengeCapGemini — incident analysis pipeline for PV and wind assets."""

import argparse

from datachallengecapgemini.plot_factory import (
    PlotFactory,
    SolarPlotFactory,
    WindPlotFactory,
)
from datachallengecapgemini.preprocessing import (
    ocr_directory,
    ocr_pdf,
    parse_ocr_directory,
    parse_ocr_json,
)
from datachallengecapgemini.report_factory import (
    ReportFactory,
    SolarReportFactory,
    WindReportFactory,
)

__all__ = [
    "PlotFactory",
    "ReportFactory",
    "SolarPlotFactory",
    "SolarReportFactory",
    "WindPlotFactory",
    "WindReportFactory",
    "ocr_directory",
    "ocr_pdf",
    "parse_ocr_directory",
    "parse_ocr_json",
]


def main() -> None:
    """CLI entry point — ``uv run datachallengecapgemini``."""
    from datachallengecapgemini.clustering import (
        ClusteringArgs,
        add_clustering_arguments,
        run_clustering,
    )
    from datachallengecapgemini.pdf_export import (
        add_pdf_arguments,
        run_pdf_export,
    )
    from datachallengecapgemini.plot_factory import (
        add_plotting_arguments,
        run_plotting,
    )
    from datachallengecapgemini.preprocessing import (
        PreprocessingArgs,
        add_preprocessing_arguments,
        run_preprocessing,
    )
    from datachallengecapgemini.report_factory import (
        add_report_arguments,
        run_reporting,
    )

    parser = argparse.ArgumentParser(
        description="The CLI entry point for the whole pipeline, from preprocessing to report generation"
    )

    parser.add_argument(
        "--with-preprocessing",
        action="store_true",
        help="If we should run the preprocessing or not",
    )

    add_preprocessing_arguments(
        parser
    )  # adding preprocessing specific aguments to the preprocessing specific parser
    add_clustering_arguments(
        parser
    )  # adding clustering specific arguments to the pipeline parser
    add_plotting_arguments(
        parser
    )  # adding plotting specific arguments to the pipeline parser
    add_report_arguments(
        parser
    )  # adding report generation specific arguments to the pipeline parser
    add_pdf_arguments(
        parser
    )  # adding PDF export specific arguments to the pipeline parser

    args = parser.parse_args()

    if args.with_preprocessing:
        args_to_use = PreprocessingArgs(
            input_dir=args.input_dir,
            digital_input_dir=args.digital_input_dir,
            output_dir=args.output_dir,
            limit=args.limit,
            force=args.force,
            output_csv=args.output_csv,
            output_digital_csv=args.output_digital_csv,
            output_merged_csv=args.output_merged_csv,
            reference_csv=args.reference_csv,
        )
        run_preprocessing(args_to_use)

    else:
        print(
            "Skipping preprocessing, assuming the merged incidents CSV "
            f"already exists at {args.clustering_input_csv}..."
        )

    if args.skip_clustering:
        print(
            "Skipping clustering, assuming the clusterised solar and wind "
            f"CSVs already exist at {args.solar_csv} and {args.wind_csv}..."
        )
    else:
        print()
        print("=" * 60)
        print("Clustering: topic modeling of solar and wind incidents")
        print("=" * 60)
        run_clustering(
            ClusteringArgs(
                input_csv=args.clustering_input_csv,
                solar_output_csv=args.solar_csv,
                wind_output_csv=args.wind_csv,
                min_cluster_size_start=args.min_cluster_size_start,
                max_cluster_size_fraction=args.max_cluster_size_fraction,
                min_cluster_size_step=args.min_cluster_size_step,
            )
        )

    print()
    print("=" * 60)
    print("Plotting: generating separate solar and wind plots")
    print("=" * 60)
    run_plotting(args.solar_csv, args.wind_csv, args.plots_output_dir)

    print()
    print("=" * 60)
    print("Reporting: filling solar and wind markdown templates")
    print("=" * 60)
    run_reporting(
        args.solar_csv,
        args.wind_csv,
        args.plots_output_dir,
        args.templates_dir,
        args.reports_output_dir,
    )

    if args.skip_pdf:
        print("Skipping PDF export (--skip-pdf)...")
    else:
        print()
        print("=" * 60)
        print("PDF export: converting markdown reports to PDF with pandoc")
        print("=" * 60)
        run_pdf_export(args.reports_output_dir)
