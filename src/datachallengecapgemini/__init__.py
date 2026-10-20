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


def main_equipment() -> None:
    """CLI entry point — ``uv run dc-equipment --site OUEST1``.

    Per-equipment reports for one site: plot_factory writes the figures and
    JSON of every selected equipment, then report_factory runs one Azure
    OpenAI agent per report section and assembles the report.
    """
    from datachallengecapgemini.equipment_stats import (
        compute_criticality,
        has_failure_modes,
        load_solar_incidents,
        select_equipment,
        site_code,
    )
    from datachallengecapgemini.plot_factory import (
        add_equipment_plotting_arguments,
        run_equipment_plotting,
    )
    from datachallengecapgemini.report_factory import (
        add_equipment_report_arguments,
        run_equipment_reporting,
    )

    parser = argparse.ArgumentParser(
        description="Per-equipment incident reports (solar), one Azure OpenAI agent per section"
    )
    parser.add_argument(
        "--site", required=True, help="Site code (e.g. OUEST1) or full site name."
    )
    parser.add_argument(
        "--equipment",
        nargs="+",
        help="Report on these equipment only (default: the critical equipment of the site).",
    )
    parser.add_argument(
        "--all-equipment",
        action="store_true",
        help="Report on every equipment of the site, not only the critical ones.",
    )
    add_equipment_plotting_arguments(parser)
    add_equipment_report_arguments(parser)
    args = parser.parse_args()

    df = load_solar_incidents(args.solar_csv)
    criticality = compute_criticality(df)
    equipment_ids = select_equipment(
        criticality, args.site, args.equipment, args.all_equipment
    )
    skipped = [e for e in equipment_ids if not has_failure_modes(df, e)]
    equipment_ids = [e for e in equipment_ids if e not in skipped]
    if skipped:
        print(
            "Skipping (no moderate or severe incident with a failure mode): "
            + ", ".join(skipped)
        )
    if not equipment_ids:
        print("No equipment to report on.")
        return

    site_dir = args.equipment_output_dir / site_code(equipment_ids[0])
    site_dir.mkdir(parents=True, exist_ok=True)
    on_site = criticality[criticality["equipment_id"].map(site_code) == site_dir.name]
    on_site.to_csv(site_dir / "criticality.csv", index=False)
    print(f"{len(equipment_ids)} equipment: {', '.join(equipment_ids)}")

    print()
    print("=" * 60)
    print("Plotting: figures and JSON per equipment")
    print("=" * 60)
    run_equipment_plotting(df, criticality, equipment_ids, site_dir)

    print()
    print("=" * 60)
    print("Reporting: one Azure OpenAI agent per report section")
    print("=" * 60)
    run_equipment_reporting(
        equipment_ids,
        site_dir,
        args.templates_dir,
        language=args.language,
        dry_run=args.dry_run,
        force=args.force,
        pdf=args.pdf,
    )
