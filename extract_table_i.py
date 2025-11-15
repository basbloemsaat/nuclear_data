#!/usr/bin/env python3
"""
Extract Table I from NUBASE2020.pdf
"""

import pdfplumber
import pandas as pd
import re
from pathlib import Path

def extract_table_i(pdf_path):
    """Extract Table I from the NUBASE2020 PDF"""
    
    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Search for "Table I" in the document
        table_found = False
        table_data = []
        
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            
            if text and "Table I" in text:
                print(f"Found 'Table I' on page {page_num + 1}")
                
                # Extract tables from this page
                tables = page.extract_tables()
                
                for i, table in enumerate(tables):
                    if table:
                        print(f"\nTable {i+1} on page {page_num + 1}:")
                        print("=" * 50)
                        
                        # Convert to DataFrame for better display
                        df = pd.DataFrame(table)
                        print(df.to_string(index=False))
                        
                        # Save the table data
                        table_data.append({
                            'page': page_num + 1,
                            'table_index': i + 1,
                            'data': table
                        })
                        
                        table_found = True
                
                # Also print the text context around "Table I"
                lines = text.split('\n')
                for j, line in enumerate(lines):
                    if "Table I" in line:
                        print(f"\nContext around 'Table I' on page {page_num + 1}:")
                        print("=" * 50)
                        start = max(0, j - 5)
                        end = min(len(lines), j + 15)
                        for k in range(start, end):
                            marker = " >>> " if k == j else "     "
                            print(f"{marker}{lines[k]}")
                        print("=" * 50)
        
        if not table_found:
            print("Table I not found. Searching for any tables in the first few pages...")
            
            # Look at first 10 pages for any tables
            for page_num in range(min(10, len(pdf.pages))):
                page = pdf.pages[page_num]
                tables = page.extract_tables()
                
                if tables:
                    print(f"\nFound {len(tables)} table(s) on page {page_num + 1}")
                    for i, table in enumerate(tables):
                        if table and len(table) > 1:  # Skip single-row tables
                            print(f"\nTable {i+1} on page {page_num + 1}:")
                            print("=" * 50)
                            df = pd.DataFrame(table)
                            print(df.to_string(index=False))
                            
                            table_data.append({
                                'page': page_num + 1,
                                'table_index': i + 1,
                                'data': table
                            })
    
    return table_data

def save_table_as_csv(table_data, output_dir):
    """Save extracted tables as CSV files"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for table_info in table_data:
        filename = f"table_page_{table_info['page']}_table_{table_info['table_index']}.csv"
        filepath = output_path / filename
        
        df = pd.DataFrame(table_info['data'])
        df.to_csv(filepath, index=False, header=False)
        print(f"Saved table to: {filepath}")

if __name__ == "__main__":
    pdf_path = "/home/bas/src/nuclear_data/data_sources/NUBASE2020.pdf"
    output_dir = "/home/bas/src/nuclear_data/data"
    
    print("Extracting Table I from NUBASE2020.pdf...")
    table_data = extract_table_i(pdf_path)
    
    if table_data:
        print(f"\nFound {len(table_data)} table(s) total")
        save_table_as_csv(table_data, output_dir)
    else:
        print("No tables found.")