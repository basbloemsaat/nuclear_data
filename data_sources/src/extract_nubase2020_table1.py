from pathlib import Path

import pdfplumber


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

SUPERSCRIPT_MAP = {
    "i": "ⁱ",
    "j": "ʲ",
    "m": "ᵐ",
    "n": "ⁿ",
    "p": "ᵖ",
    "q": "۹",
    "r": "ʳ",
    "s": "ˢ",
}


def convert_to_superscript(s: str) -> str:
    """
    Converts a string to its superscript equivalent.
    """
    return "".join(SUPERSCRIPT_MAP.get(char, char) for char in s)


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

    # Post-process lines to fix superscripts
    # pdfplumber does not always correctly extract superscripts.
    # For now, we only fix the β− case.
    processed_lines = [line.replace("β−", "β⁻") for line in final_lines]

    # Merge lines that were split
    merged_lines = []
    for line in processed_lines:
        # The first column is the nuclide, which always starts with a number (or '2p')
        # If a line does not start with a number (or is empty), it is a continuation of the previous line.
        if (line.strip() and not line.strip()[0].isdigit()) or line.strip().startswith(
            "2p"
        ):
            if merged_lines:
                # insert line right after the previous line's last semicolon
                last_semicolon_index = merged_lines[-1].rfind(";")
                if last_semicolon_index != -1:
                    merged_lines[-1] = (
                        merged_lines[-1][: last_semicolon_index + 1]
                        + line.strip()
                        + " "
                        + merged_lines[-1][last_semicolon_index + 1 :].strip()
                    )


                # merged_lines[-1] += f" {line.strip()}"
        else:
            merged_lines.append(line)

    # Convert nuclide suffixes to superscripts
    suffixed_lines = []
    for i, line in enumerate(merged_lines):
        if i > 0:
            prev_line = suffixed_lines[i - 1]
            current_nuclide = line.split()[0]
            prev_nuclide = prev_line.split()[0]

            current_element = "".join(filter(str.isalpha, current_nuclide))
            prev_element = "".join(filter(str.isalpha, prev_nuclide))

            print(
                f"  Current element: {current_element, prev_element} , comparison: {prev_element[:-1]} "
            )

            if current_element.startswith(
                prev_element[:-1]
            ) and current_nuclide.startswith(prev_nuclide[:-1]):
                suffix = current_nuclide[-1]
                print(f"  Found suffix: {suffix}")
                if suffix:
                    superscript_suffix = convert_to_superscript(suffix)
                    new_nuclide = current_nuclide[:-1] + superscript_suffix
                    line = line.replace(current_nuclide, new_nuclide, 1)
        suffixed_lines.append(line)

    with open(TXT_PATH, "w", encoding="utf-8") as f:
        for line in suffixed_lines:
            f.write(line + "\n")
    print(
        f"Successfully extracted and filtered {len(suffixed_lines)} lines to {TXT_PATH}"
    )
