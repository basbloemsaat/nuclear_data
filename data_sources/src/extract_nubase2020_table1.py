import os
import sys
import csv
from pathlib import Path
from typing import List

try:
    import camelot
except ImportError:
    print("camelot not found. Please install it with 'pip install camelot-py[cv]'.")
    sys.exit(1)

PDF_PATH = Path(__file__).parent.parent / "NUBASE2020.pdf"
OUTPUT_DIR = Path(__file__).parent.parent / "tmp"
OUTPUT_DIR.mkdir(exist_ok=True)
CSV_PATH = OUTPUT_DIR / "NUBASE2020_TableI.csv"

TABLE1_START_PAGE = 21  # 1-based page number
TABLE1_END_PAGE = 21  # inclusive
# Canonical header for Table I (two-line header combined)
TABLE1_HEADER = [
    'Nuclide',
    'Mass excess (keV)',
    'Excitation Energy (keV)',
    'Half-life',
    'Jπ',
    'Ens Reference',
    'Year of discovery',
    'Decay modes and intensities (%)',
]


def _replace_ligatures_and_normalize(s: str) -> str:
    import unicodedata

    if not s:
        return s
    # replace common ligatures and normalize to NFC
    s = s.replace('\ufb01', 'fi').replace('\ufb02', 'fl')
    return unicodedata.normalize('NFC', s)


def extract_table_from_pdf(pdf_path: Path, start_page: int, end_page: int) -> List[List[str]]:
    """Extract tables from `pdf_path` pages `start_page`..`end_page` (1-based).

    Treat each page as a separate table, concatenate rows, ignore lines
    starting with '*' (footnotes), and return list of rows (each row is list[str]).
    """
    all_rows: List[List[str]] = []
    header_row: List[str] = []
    # For Table I start page, prefer the canonical header
    if start_page == TABLE1_START_PAGE:
        header_row = list(TABLE1_HEADER)

    # Try camelot first (good for lattice/stream tables). Each page is handled
    # separately so we can stop after verifying page 21.
    try:
        import camelot

        for p in range(start_page, end_page + 1):
            tables = camelot.read_pdf(str(pdf_path), pages=str(p), flavor='stream')
            if not tables:
                continue
            # concatenate tables on that page
            for t in tables:
                df = t.df
                for ridx, row in df.iterrows():
                    # join cells with a single space, then split on multiple spaces
                    joined = ' '.join([str(c).strip() for c in row.tolist()])
                    joined = _replace_ligatures_and_normalize(joined)
                    if joined.startswith('*'):
                        continue
                    # split by two or more spaces to heuristically separate columns
                    parts = [p for p in [c.strip() for c in joined.split('  ')] if p]
                    if not parts:
                        continue
                    # Attempt to detect the two-line header at the top of the first
                    # processed page. We expect the header to be two lines of text
                    # (e.g. column names and units) that contain alphabetic tokens.
                    if p == start_page and not header_row:
                        # Collect candidate header lines: the first two text rows
                        # that contain letters and not predominantly numeric data.
                        import re

                        def looks_like_header(parts: List[str]) -> bool:
                            joined = ' '.join(parts)
                            # must contain at least one alpha char
                            return bool(re.search(r'[A-Za-zα-ωΑ-Ωµµ]', joined))

                        # if this is one of the first two rows, treat as header
                        if ridx in (0, 1) or (len(header_row) < 2 and looks_like_header(parts)):
                            header_row.append(' '.join(parts))
                            # only add header when we have two lines combined
                            if len(header_row) == 2:
                                # join header lines into columns by splitting on multiple spaces
                                h0 = header_row[0]
                                h1 = header_row[1]
                                # split into columns by two or more spaces
                                cols0 = [c for c in [x.strip() for x in re.split(r"\s{2,}", h0)] if c]
                                cols1 = [c for c in [x.strip() for x in re.split(r"\s{2,}", h1)] if c]
                                # If counts match, combine per-column; else place both lines in first header cell
                                if len(cols0) == len(cols1) and len(cols0) > 1:
                                    header_row = [f"{a} {b}".strip() for a, b in zip(cols0, cols1)]
                                else:
                                    header_row = [f"{h0} {h1}".strip()]
                            continue
                        else:
                            all_rows.append(parts)
                    else:
                        all_rows.append(parts)
    except Exception:
        # If camelot is unavailable or fails, fallback to simple text extraction
        from pdfminer.high_level import extract_text

        text = extract_text(str(pdf_path), page_numbers=list(range(start_page - 1, end_page)))
        for ln in text.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith('*'):
                continue
            ln = _replace_ligatures_and_normalize(ln)
            # heuristic split on multiple spaces or tab
            parts = [p for p in [c.strip() for c in __import__('re').split(r"\s{2,}|\t", ln)] if p]
            if parts:
                # For text fallback, treat first two non-empty text lines as header
                if start_page and not header_row:
                    header_row.append(' '.join(parts))
                    if len(header_row) == 2:
                        import re
                        cols0 = [c for c in [x.strip() for x in re.split(r"\s{2,}", header_row[0])] if c]
                        cols1 = [c for c in [x.strip() for x in re.split(r"\s{2,}", header_row[1])] if c]
                        if len(cols0) == len(cols1) and len(cols0) > 1:
                            header_row = [f"{a} {b}".strip() for a, b in zip(cols0, cols1)]
                        else:
                            header_row = [f"{header_row[0]} {header_row[1]}".strip()]
                    continue
                all_rows.append(parts)

    # If we used a canonical TABLE1_HEADER, drop any leading rows that look
    # like the source two-line header so we don't duplicate it in the CSV.
    if header_row:
        # ensure header is list[str]
        if isinstance(header_row, list) and header_row:
            if len(header_row) == 1 and isinstance(header_row[0], str):
                import re

                cols = [c for c in [x.strip() for x in re.split(r"\s{2,}", header_row[0])] if c]
                header_row = cols if cols else header_row

        # If header_row equals the canonical header, remove leading source header rows
        if header_row == list(TABLE1_HEADER):
            def looks_like_source_header(r: List[str]) -> bool:
                s = ' '.join(r).lower()
                keywords = ['nuclide', 'mass excess', 'excitation energy', 'half-life', 'jπ', 'decay']
                return any(k in s for k in keywords)

            # drop up to first 3 leading rows that match
            drop = 0
            for r in list(all_rows[:3]):
                if looks_like_source_header(r):
                    drop += 1
                else:
                    break
            if drop:
                all_rows = all_rows[drop:]

        all_rows.insert(0, header_row)

    return all_rows


def _write_csv(rows: List[List[str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)


if __name__ == '__main__':
    # Simple CLI to extract a page range and write CSV (used to extract page 21)
    rows = extract_table_from_pdf(PDF_PATH, TABLE1_START_PAGE, TABLE1_END_PAGE)
    _write_csv(rows, CSV_PATH)
    print('Wrote', CSV_PATH, 'rows=', len(rows))
