import pdfplumber
from pathlib import Path


PDF_PATH = Path(__file__).parent.parent / "NUBASE2020.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "tmp"
OUTPUT_DIR.mkdir(exist_ok=True)
CSV_PATH = OUTPUT_DIR / "NUBASE2020_TableI.csv"

TABLE1_START_PAGE = 21  # 1-based page number
TABLE1_END_PAGE = 181  # inclusive
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


def extract_table_from_pdf(pdf_path: Path, start_page: int, end_page: int) -> list[str]:
    """
    Extracts table data from a PDF file, page by page, line by line.
    This version uses `extract_words` to reconstruct lines with proper spacing.

    Args:
        pdf_path: Path to the PDF file.
        start_page: The first page to extract (1-based).
        end_page: The last page to extract (inclusive).

    Returns:
        A list of lines as strings.
    """
    all_lines: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        # pdfplumber pages are 0-indexed
        pages_to_extract = range(start_page - 1, end_page)
        for page_num in pages_to_extract:
            page = pdf.pages[page_num]
            # The `layout=True` and `keep_blank_chars` arguments to `extract_text`
            # were not sufficient.
            # A more robust method is to extract words and reconstruct the lines.
            text = page.extract_text(x_tolerance=1, y_tolerance=1)
            if text:
                all_lines.extend(text.splitlines())
    return all_lines


if __name__ == "__main__":
    TXT_PATH = OUTPUT_DIR / "NUBASE2020_TableI.txt"
    extracted_lines = extract_table_from_pdf(
        PDF_PATH, TABLE1_START_PAGE, TABLE1_END_PAGE
    )
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        for line in extracted_lines:
            f.write(line + "\n")
    print(f"Successfully extracted {len(extracted_lines)} lines to {TXT_PATH}")
