import csv
import re
from pathlib import Path

# Define the headers for the CSV file
HEADERS = [
    "Nuclide",
    "Mass Excess (keV)",
    "Excitation Energy (keV)",
    "Half-life",
    "Jπ",
    "Ens Reference",
    "Year of discovery",
    "Decay modes and intensities (%)",
]


# Define the input and output file paths
INPUT_FILE = Path(__file__).parent.parent / "tmp" / "NUBASE2020_TableI.txt"
OUTPUT_FILE = Path(__file__).parent.parent / "tmp" / "nubase2020_table1.csv"


def clean_and_parse_line(line):
    """
    Clean and parse a single line of text into structured data.
    """
    # Example regex to split the line into fields (adjust as needed)
    fields = re.split(r"\s{2,}", line.strip())

    # Ensure the number of fields matches the headers
    if len(fields) != len(HEADERS):
        raise ValueError(f"Unexpected number of fields: {fields}")

    return fields


def process_file(input_file: Path, output_file: Path):
    """
    Process the input file and write the cleaned data to a CSV file.
    """
    with (
        open(input_file, "r", encoding="utf-8") as infile,
        open(output_file, "w", newline="", encoding="utf-8") as outfile,
    ):
        csv_writer = csv.writer(outfile)

        # Write the headers to the CSV file
        csv_writer.writerow(HEADERS)

        for line in infile:
            # Skip empty lines or lines starting with an asterisk (*)
            if not line.strip() or line.startswith("*"):
                continue

            print(line.strip())

            # try:
            #     # Clean and parse the line
            #     parsed_line = clean_and_parse_line(line)

            #     # Write the parsed line to the CSV file
            #     csv_writer.writerow(parsed_line)
            # except ValueError as e:
            #     print(f"Skipping line due to error: {e}")


if __name__ == "__main__":
    process_file(INPUT_FILE, OUTPUT_FILE)
