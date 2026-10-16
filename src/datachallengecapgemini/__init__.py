"""DataChallengeCapGemini — incident analysis pipeline for PV and wind assets."""

import argparse

from datachallengecapgemini.plot_factory import PlotFactory
from datachallengecapgemini.preprocessing import (
    ocr_directory,
    ocr_pdf,
    parse_ocr_directory,
    parse_ocr_json,
)

__all__ = [
    "PlotFactory",
    "ocr_directory",
    "ocr_pdf",
    "parse_ocr_directory",
    "parse_ocr_json",
]


def main() -> None:
    """CLI entry point — ``uv run datachallengecapgemini``."""
    from datachallengecapgemini.plot_factory import (
        add_plotting_arguments,
        run_plotting,
    )
    from datachallengecapgemini.preprocessing import (
        PreprocessingArgs,
        add_preprocessing_arguments,
        run_preprocessing,
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
    add_plotting_arguments(
        parser
    )  # adding plotting specific arguments to the pipeline parser

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
            f"Skipping preprocessing, assuming the merged csv is in {args.output_merged_csv}..."
        )

    print()
    print("=" * 60)
    print("Plotting: generating plots from the merged CSV")
    print("=" * 60)
    run_plotting(args.output_merged_csv, args.plots_output_dir)
