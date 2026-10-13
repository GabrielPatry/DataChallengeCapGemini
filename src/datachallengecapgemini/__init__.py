"""DataChallengeCapGemini — incident analysis pipeline for PV and wind assets."""

from datachallengecapgemini.preprocessing import (
    ocr_directory,
    ocr_pdf,
    parse_ocr_directory,
    parse_ocr_json,
)

__all__ = [
    "ocr_directory",
    "ocr_pdf",
    "parse_ocr_directory",
    "parse_ocr_json",
]


def main() -> None:
    """CLI entry point — ``uv run datachallengecapgemini``."""
    from datachallengecapgemini.preprocessing import main as _preprocess_main

    _preprocess_main()
