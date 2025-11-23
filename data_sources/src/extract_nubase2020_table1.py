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
            text = page.extract_text(x_tolerance=1, y_tolerance=3)
            if text:
                all_lines.extend(text.splitlines())
    return all_lines


if __name__ == "__main__":
    TXT_PATH = OUTPUT_DIR / "NUBASE2020_TableI.txt"
    extracted_lines = extract_table_from_pdf(
        PDF_PATH, TABLE1_START_PAGE, TABLE1_END_PAGE
    )
    # Filter out lines starting with '∗'
    filtered_lines = [
        line for line in extracted_lines if not line.strip().startswith("∗")
    ]

    header_lines_to_remove = {
        "Chinese Physics C Vol. 45, No. 3 (2021) 030001",
        "Table I. The NUBASE2020 table (Explanation of Table on page 030001-16)",
        "Nuclide Mass excess Excitation Energy Half-life Jπ Ens Reference Year of Decay modes and intensities",
        "(keV) (keV) discovery (%)",
    }

    final_lines = [
        line
        for line in filtered_lines
        if line.strip() not in header_lines_to_remove
        and not line.strip().startswith("030001-")
    ]

    with open(TXT_PATH, "w", encoding="utf-8") as f:
        for line in final_lines:
            f.write(line + "\n")
    print(f"Successfully extracted and filtered {len(final_lines)} lines to {TXT_PATH}")
