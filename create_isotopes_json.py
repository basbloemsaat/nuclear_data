#!/usr/bin/env python3
"""
Create a JSON file of isotopes with atomic number (Z), mass number (A), 
symbol, and element name from the complete isotope database.
"""

import pandas as pd
import json

def main():
    print("Creating JSON file of isotopes...")
    
    # Read the complete isotope database
    df = pd.read_csv('data/complete_isotope_database.csv')
    print(f"Reading {len(df)} isotopes from database")
    
    # Create list of isotopes with requested fields
    isotopes = []
    
    for _, row in df.iterrows():
        isotope = {
            "Z": int(row['Atomic_Number']) if pd.notna(row['Atomic_Number']) else 0,
            "A": int(row['Mass_Number']) if pd.notna(row['Mass_Number']) else None,
            "Symbol": row['Symbol'],
            "Element_Name": row['Element_Name']
        }
        isotopes.append(isotope)
    
    # Sort by atomic number, then mass number
    isotopes.sort(key=lambda x: (x['Z'], x['A'] if x['A'] is not None else 0))
    
    # Create the JSON structure
    isotope_data = {
        "metadata": {
            "title": "Nuclear Isotope Database",
            "description": "Complete list of isotopes with atomic number (Z), mass number (A), symbol, and element name",
            "source": "NUBASE2020 + Wikipedia Chemical Elements",
            "total_isotopes": len(isotopes),
            "date_created": "2025-11-15",
            "fields": {
                "Z": "Atomic number (number of protons)",
                "A": "Mass number (protons + neutrons)", 
                "Symbol": "Chemical element symbol",
                "Element_Name": "Full element name"
            }
        },
        "isotopes": isotopes
    }
    
    # Save to JSON file
    output_file = 'data/isotopes.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(isotope_data, f, indent=2, ensure_ascii=False)
    
    print(f"JSON file created: {output_file}")
    print(f"Total isotopes: {len(isotopes)}")
    
    # Show some statistics
    elements = set(isotope['Symbol'] for isotope in isotopes)
    print(f"Elements represented: {len(elements)}")
    
    z_range = [isotope['Z'] for isotope in isotopes if isotope['Z'] is not None]
    a_range = [isotope['A'] for isotope in isotopes if isotope['A'] is not None]
    
    print(f"Atomic number range: {min(z_range)} to {max(z_range)}")
    print(f"Mass number range: {min(a_range)} to {max(a_range)}")
    
    # Show first few entries
    print(f"\nFirst 10 isotopes:")
    for i, isotope in enumerate(isotopes[:10]):
        print(f"  {i+1:2d}. Z={isotope['Z']:3d}, A={isotope['A']:3d}, {isotope['Symbol']:2s} ({isotope['Element_Name']})")
    
    # Show some heavy isotopes
    print(f"\nLast 5 isotopes (heaviest):")
    for i, isotope in enumerate(isotopes[-5:], len(isotopes)-4):
        print(f"  {i:2d}. Z={isotope['Z']:3d}, A={isotope['A']:3d}, {isotope['Symbol']:2s} ({isotope['Element_Name']})")

if __name__ == "__main__":
    main()