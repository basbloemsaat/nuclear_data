from pathlib import Path

import pdfplumber


PDF_PATH = Path(__file__).parent.parent / "NUBASE2020.pdf"
TXT_PATH = Path(__file__).parent.parent / "tmp" / "nubase2020_table_ws.txt"

TABLE1_START_PAGE = 21  # 1-based page number
TABLE1_END_PAGE = 181  # inclusive

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
    """Extracts table from PDF, preserving whitespace."""
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        # Page numbers in pdfplumber are 0-based
        for i in range(start_page - 1, end_page):
            page = pdf.pages[i]
            # layout=True preserves the layout of the text on the page.
            text = page.extract_text(layout=True, x_tolerance=1, y_tolerance=3)
            if text:
                all_text.append(text)

        # Flatten the list of strings into a single list of lines
        extracted_lines = [
            line.strip()
            for page_text in all_text
            for line in page_text.splitlines()
            if line.strip()
        ]

        filtered_lines = [
            line for line in extracted_lines if not line.strip().startswith("∗")
        ]

        print(f"Extracted {len(filtered_lines)} lines after filtering.")

        header_lines_to_remove = {
            "Chinese Physics C Vol. 45, No. 3 (2021) 030001",
            "Table I. The NUBASE2020 table (Explanation of Table on page 030001-16)",
            "Nuclide Mass excess Excitation Energy Half-life Jπ Ens Reference Year of Decay modes and intensities",
            "(keV) (keV) discovery (%)",
            "(keV)       (keV)                          discovery (%)",
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
            if (
                line.strip() and not line.strip()[0].isdigit()
            ) or line.strip().startswith("2p"):
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

                if current_element.startswith(
                    prev_element[:-1]
                ) and current_nuclide.startswith(prev_nuclide[:-1]):
                    suffix = current_nuclide[-1]
                    if suffix:
                        superscript_suffix = convert_to_superscript(suffix)
                        new_nuclide = current_nuclide[:-1] + superscript_suffix
                        line = line.replace(current_nuclide, new_nuclide, 1)
            suffixed_lines.append(line)

    return suffixed_lines


if __name__ == "__main__":
    table_pages = extract_table_from_pdf(PDF_PATH, TABLE1_START_PAGE, TABLE1_END_PAGE)
    TXT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(table_pages))

    print(f"Successfully extracted table to {TXT_PATH}")
