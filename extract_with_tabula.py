#!/usr/bin/env python3
"""
Extract Table I from NUBASE2020.pdf using tabula-py
"""

import tabula
import pandas as pd
from pathlib import Path

def extract_table_with_tabula(pdf_path):
    """Extract tables using tabula-py"""
    
    print("Attempting to extract tables using tabula-py...")
    
    # Try to extract all tables from the PDF
    try:
        # Extract tables from all pages
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        print(f"Found {len(tables)} tables using tabula-py")
        
        for i, table in enumerate(tables):
            if not table.empty:
                print(f"\nTable {i+1}:")
                print("=" * 50)
                print(table.head(10))  # Show first 10 rows
                print(f"Shape: {table.shape}")
                
                # Save each table
                output_file = f"/home/bas/src/nuclear_data/data/tabula_table_{i+1}.csv"
                table.to_csv(output_file, index=False)
                print(f"Saved to: {output_file}")
        
        return tables
        
    except Exception as e:
        print(f"Error with tabula-py: {e}")
        return []

def extract_specific_pages(pdf_path, pages):
    """Extract tables from specific pages"""
    
    print(f"Extracting tables from pages: {pages}")
    
    try:
        tables = tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True)
        
        for i, table in enumerate(tables):
            if not table.empty:
                print(f"\nTable {i+1} from pages {pages}:")
                print("=" * 50)
                print(table.head())
                print(f"Shape: {table.shape}")
                
                # Save table
                output_file = f"/home/bas/src/nuclear_data/data/specific_table_{i+1}.csv"
                table.to_csv(output_file, index=False)
                print(f"Saved to: {output_file}")
        
        return tables
        
    except Exception as e:
        print(f"Error extracting from specific pages: {e}")
        return []

if __name__ == "__main__":
    pdf_path = "/home/bas/src/nuclear_data/data_sources/NUBASE2020.pdf"
    
    # First try extracting from all pages
    all_tables = extract_table_with_tabula(pdf_path)
    
    # If that doesn't work well, try specific pages where we found "Table I" references
    if not all_tables or all([table.empty for table in all_tables]):
        print("\nTrying specific pages where Table I was mentioned...")
        specific_tables = extract_specific_pages(pdf_path, "3,6,8,11,13,14")
    
    # Try a more targeted approach for the first few pages
    print("\nTrying first 10 pages with different settings...")
    try:
        tables_first_10 = tabula.read_pdf(
            pdf_path, 
            pages="1-10", 
            multiple_tables=True,
            lattice=True,  # Try lattice mode
            pandas_options={'header': None}
        )
        
        for i, table in enumerate(tables_first_10):
            if not table.empty and table.shape[0] > 5:  # Only show tables with more than 5 rows
                print(f"\nLattice Table {i+1} (pages 1-10):")
                print("=" * 50)
                print(table.head(10))
                print(f"Shape: {table.shape}")
                
                output_file = f"/home/bas/src/nuclear_data/data/lattice_table_{i+1}.csv"
                table.to_csv(output_file, index=False)
                print(f"Saved to: {output_file}")
                
    except Exception as e:
        print(f"Error with lattice mode: {e}")