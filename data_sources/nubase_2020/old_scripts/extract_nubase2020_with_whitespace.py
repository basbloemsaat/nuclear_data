import json
import re
from pathlib import Path

import pdfplumber

PDF_PATH = Path(__file__).parent.parent / "NUBASE2020.pdf"
TXT_PATH = Path(__file__).parent.parent / "tmp" / "nubase2020_table_ws.txt"

TABLE1_START_PAGE = 22  # 21
TABLE1_END_PAGE = 23  # 181  # inclusive

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
    """Converts a string to its superscript equivalent."""

    return "".join(SUPERSCRIPT_MAP.get(char, char) for char in s)


def extract_int_from_string(input_string: str) -> int:
    """Extracts number from the beginning of a string."""

    first_part = re.split(r"[^0-9]", input_string.strip(), maxsplit=0, flags=0)[0]
    if not first_part:
        return 0
    return int(first_part)


def extract_float_from_string(input_string: str) -> int:
    """Extracts number from the beginning of a string."""

    first_part = re.split(r"[^0-9\.-]", input_string.strip(), maxsplit=0, flags=0)[0]
    if not first_part:
        return 0
    return float(first_part)


def extract_table_from_pdf(pdf_path: Path, start_page: int, end_page: int) -> list[str]:
    """Extracts table from PDF, preserving whitespace."""

    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        # Page numbers in pdfplumber are 0-based
        for i in range(start_page - 1, end_page):
            page = pdf.pages[i]
            # layout=True preserves the layout of the text on the page.
            text = page.extract_text(
                layout=True, x_tolerance=1, y_tolerance=3, x_density=2, y_density=2
            )
            if text:
                all_text.append(text)

        # Flatten the list of strings into a single list of lines
        extracted_lines = [
            line.strip()
            for page_text in all_text
            for line in page_text.splitlines()
            if line.strip()
        ]

        # Filter out lines that start with "∗", those are footnotes
        filtered_lines = [
            line for line in extracted_lines if not line.strip().startswith("∗")
        ]

        # for later, we don't do anything with these yet
        comment_lines = [
            line for line in extracted_lines if line.strip().startswith("∗")
        ]

        # Remove header/footer lines that repeat on each page
        header_lines_to_remove = {
            "Chinese Physics C Vol. 45, No. 3 (2021) 030001",
            "Table I. The NUBASE2020 table (Explanation of Table on page 030001-16)",
            "Nuclide Mass excess Excitation Energy Half-life Jπ Ens Reference Year of Decay modes and intensities",
            "(keV) (keV) discovery (%)",
            "(keV)       (keV)                          discovery (%)",
            "Chinese       Physics      C   Vol.   45,   No.    3  (2021)      030001",
            "Table      I.  The      NUBASE2020                 table      (Explanation              of   Table      on    page      030001-16)",
            "Nuclide             Mass    excess                       Excitation      Energy                            Half-life                          Jπ        Ens    Reference          Year   of           Decay    modes     and   intensities",
            "(keV)                                     (keV)                                                                                                           discovery                            (%)",
        }

        final_lines = [
            line
            for line in filtered_lines
            if line.strip() not in header_lines_to_remove
            and not line.strip().startswith("030001-")
        ]

        # if the last character is "*", remove it (footnote marker)
        final_lines = [
            line[:-1] if line.endswith("∗") else line for line in final_lines
        ]

        # Post-process lines to fix superscripts and other issues.
        # pdfplumber does not always correctly extract superscripts.
        # For now, we only fix the β⁻ case.
        processed_lines = [line.replace("β−", "β⁻") for line in final_lines]
        processed_lines = [line.replace("β+", "β⁺") for line in processed_lines]
        processed_lines = [line.replace("−", "-") for line in processed_lines]
        processed_lines = [line.replace("∗", "*") for line in processed_lines]

        # Merge lines that were split
        merged_lines = []
        for i, line in enumerate(processed_lines):
            # The first column is the nuclide, which always starts with a number (or is '2p')
            # If a line does not start with a number (or is empty), it is a continuation of the previous line.

            needs_merge = False

            if line.strip() and not line.strip()[0].isdigit():
                needs_merge = True

            if i > 0:
                prev_number = extract_int_from_string(merged_lines[-1])
                current_number = extract_int_from_string(line)

                if current_number < prev_number:
                    needs_merge = True

            if needs_merge:
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

        def nuclide_from_line(line: str) -> str:
            return line.split()[0]

        # Convert nuclide suffixes to superscripts
        suffixed_lines = []
        for i, line in enumerate(merged_lines):
            if i == 0:
                suffixed_lines.append(line)
                continue

            prev_line = suffixed_lines[i - 1]
            current_nuclide = nuclide_from_line(line)

            prev_nuclide = nuclide_from_line(prev_line)

            if current_nuclide[:-1] == prev_nuclide:
                suffix = current_nuclide[-1]
                if suffix and suffix in "ijmnpqrs":
                    line = f"{prev_nuclide:<6}{suffix:<2}{line[8:]}"

            suffixed_lines.append(line)

    return suffixed_lines


def half_life_in_seconds(value: float, unit: str) -> float:
    """Converts half-life to seconds based on unit."""
    conversion_factors = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "y": 31557600,  # average year accounting for leap years
        "ky": 3.15576e10,
        "My": 3.15576e13,
        "Gy": 3.15576e16,
        "Ty": 3.15576e19,
        "Py": 3.15576e22,
        "Ey": 3.15576e25,
        "Zy": 3.15576e28,
        "Yy": 3.15576e31,
        "ms": 1e-3,
        "μs": 1e-6,
        "ns": 1e-9,
        "ps": 1e-12,
        "fs": 1e-15,
        "as": 1e-18,
        "zs": 1e-21,
        "ys": 1e-24,
    }

    if unit in conversion_factors:
        return value * conversion_factors[unit]
    else:
        raise ValueError(f"Unknown time unit: {unit}")


def parse_half_life(half_life_str: str) -> dict[str, str | float]:
    """Parses half-life string into a structured format."""

    half_life_str = half_life_str.strip()

    half_life_data = {}

    if half_life_str == "STABLE":
        half_life_data["half_life"] = "stable"

    elif half_life_str == "p-unstable":
        half_life_data["half_life"] = "p-unstable"

    else:
        # Match number + unit
        match = re.match(
            r">?\s*([0-9.Ee\+\-]+)\s*#?\s*([a-zA-Zμ]+)\s*([0-9.Ee\+\-]+)", half_life_str
        )
        if match:
            value = float(match.group(1))
            unit = match.group(2)
            uncertainty = float(match.group(3))
            half_life_data["half_life_value"] = value
            half_life_data["half_life_unit"] = unit
            half_life_data["half_life_uncertainty"] = uncertainty
            half_life_data["half_life_seconds"] = half_life_in_seconds(value, unit)

    return half_life_data


def extract_data_from_lines(table_pages: list[str]):
    isotope_data = []
    isotope_data_lookup = {}

    for line in table_pages:
        # print(f"Processing line: {line}")

        isotope = {
            "name": line.split()[0],
            # "raw": line,
        }

        # mass excess
        mass_excess_str = line[13:28].strip()
        mass_excess = extract_float_from_string(mass_excess_str)
        isotope["mass_excess"] = mass_excess

        # mass excess uncertainty
        mass_excess_uncertainty_str = line[28:46].strip()
        mass_excess_uncertainty = extract_float_from_string(mass_excess_uncertainty_str)
        isotope["mass_excess_uncertainty"] = mass_excess_uncertainty

        # excitation energy
        excitation_energy_str = line[46:68].strip()
        if excitation_energy_str:
            excitation_energy = extract_float_from_string(excitation_energy_str)
            isotope["excitation_energy"] = excitation_energy
        else:
            isotope["excitation_energy"] = None

        # excitation energy uncertainty
        excitation_energy_uncertainty_str = line[68:82].strip()
        if excitation_energy_uncertainty_str:
            excitation_energy_uncertainty = extract_float_from_string(
                excitation_energy_uncertainty_str
            )
            isotope["excitation_energy_uncertainty"] = excitation_energy_uncertainty
        else:
            isotope["excitation_energy_uncertainty"] = None

        # exitation energy origin
        excitation_energy_origin_str = line[82:92].strip()
        if excitation_energy_origin_str:
            isotope["excitation_energy_origin"] = excitation_energy_origin_str
        else:
            isotope["excitation_energy_origin"] = None

        # half-life
        half_life_str = line[92:132]
        half_life_data = parse_half_life(half_life_str)
        isotope.update(half_life_data)

        # Jπ
        Jπ_str = line[132:152].strip()

        # replace whitespace to single space
        Jπ_str = re.sub(r"\s+", " ", Jπ_str)
        isotope["Jπ"] = Jπ_str or None

        # year of discovery
        year_of_discovery_str = line[179:187].strip()
        if year_of_discovery_str:
            year_of_discovery = extract_int_from_string(year_of_discovery_str)
            isotope["year_of_discovery"] = year_of_discovery
        else:
            isotope["year_of_discovery"] = None

        # decay modes and intensities
        decay_modes_str = line[187:].strip()
        decay_modes_str = re.sub(r"\s+", " ", decay_modes_str)

        # split by semicolon
        decay_modes = [
            mode.strip() for mode in decay_modes_str.split(";") if mode.strip()
        ]
        isotope["decay_modes"] = decay_modes

        if  isotope["name"] == "10Be": # or True:
            # print(line)
            # print(isotope)

            print(f"Isotope: {json.dumps(isotope, indent=2, ensure_ascii=False)}")
            print("---")


if __name__ == "__main__":
    table_pages = extract_table_from_pdf(PDF_PATH, TABLE1_START_PAGE, TABLE1_END_PAGE)
    TXT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(table_pages))

    print(f"Successfully extracted table to {TXT_PATH}")

    extract_data_from_lines(table_pages)
