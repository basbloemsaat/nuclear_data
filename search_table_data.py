#!/usr/bin/env python3
"""
Extract Table I from NUBASE2020.pdf by searching for the table data directly
"""

import pdfplumber
import pandas as pd
import re
from pathlib import Path

def search_for_table_i_data(pdf_path):
    """Search for Table I data in the PDF"""
    
    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF has {len(pdf.pages)} pages")
        
        # Look for pages that might contain the actual table data
        # The table typically starts after the front matter
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            if text:
                # Look for patterns that suggest nuclear data table
                # Nuclear data tables typically have entries like:
                # - Mass numbers (A)
                # - Element symbols
                # - Mass excess values
                # - Half-lives
                
                lines = text.split('\n')
                
                # Look for lines that contain nuclear data patterns
                nuclear_data_lines = []
                for line in lines:
                    # Look for patterns like: number + element symbol + mass data
                    if re.search(r'\d+[A-Z][a-z]?\s+[-\d.]+\s+\d+', line):
                        nuclear_data_lines.append(line)
                    # Or patterns with scientific notation and parentheses for uncertainties
                    elif re.search(r'\d+[A-Z][a-z]?\s+.*\(\d+\)', line):
                        nuclear_data_lines.append(line)
                
                if nuclear_data_lines:
                    print(f"\nPage {page_num + 1} - Found {len(nuclear_data_lines)} potential nuclear data lines:")
                    print("=" * 60)
                    for i, line in enumerate(nuclear_data_lines[:10]):  # Show first 10
                        print(f"{i+1:2d}: {line}")
                    if len(nuclear_data_lines) > 10:
                        print(f"... and {len(nuclear_data_lines) - 10} more lines")
                    print("=" * 60)
                
                # Also look for explicit table headers or column descriptions
                if any(keyword in text.lower() for keyword in ['nuclide', 'mass excess', 'half-life', 'ground state']):
                    print(f"\nPage {page_num + 1} contains nuclear physics terminology")
                    
                    # Look for structured data
                    if 'ground state' in text.lower():
                        # Extract lines around "ground state" mentions
                        for i, line in enumerate(lines):
                            if 'ground state' in line.lower():
                                start = max(0, i - 3)
                                end = min(len(lines), i + 8)
                                print(f"\nContext around 'ground state' on page {page_num + 1}:")
                                for j in range(start, end):
                                    marker = " >>> " if j == i else "     "
                                    print(f"{marker}{lines[j]}")
                                break

def extract_text_from_range(pdf_path, start_page, end_page):
    """Extract all text from a range of pages"""
    
    print(f"\nExtracting text from pages {start_page} to {end_page}...")
    
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        
        for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                all_text.append(f"=== PAGE {page_num + 1} ===")
                all_text.append(text)
                all_text.append("")
        
        # Save to file
        output_file = "/home/bas/src/nuclear_data/data/complete_table_text.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))
        
        print(f"Saved extracted text to: {output_file}")
        
        return '\n'.join(all_text)

if __name__ == "__main__":
    pdf_path = "/home/bas/src/nuclear_data/data_sources/NUBASE2020.pdf"
    
    print("Searching for Table I data in NUBASE2020.pdf...")
    search_for_table_i_data(pdf_path)
    
    # Extract text from the complete table (pages 21-181)
    print("\n" + "="*80)
    extract_text_from_range(pdf_path, 21, 181)  # Complete Table I from page 21 to 181