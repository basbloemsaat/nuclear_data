from pathlib import Path


PDF_PATH = Path(__file__).parent.parent / "NUBASE2020.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "tmp"
OUTPUT_DIR.mkdir(exist_ok=True)
CSV_PATH = OUTPUT_DIR / "NUBASE2020_TableI.csv"

TABLE1_START_PAGE = 21  # 1-based page number
TABLE1_END_PAGE = 21  # inclusive
# Canonical header for Table I (two-line header combined)
TABLE1_HEADER = [
    "Nuclide",
    "Mass excess (keV)",
    "Excitation Energy (keV)",
    "Half-life",
    "Jπ",
    "Ens Reference",
    "Year of discovery",
    "Decay modes and intensities (%)",
]


def extract_table_from_pdf(
    pdf_path: Path, start_page: int, end_page: int
) -> list[list[str]]: ...
