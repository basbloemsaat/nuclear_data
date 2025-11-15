#!/usr/bin/env python3
"""
Create comprehensive isotope database by combining NUBASE2020 nuclear data
with chemical elements information.

Combines:
- NUBASE2020 nuclear data (isotopes with nuclear properties)
- Chemical elements data (atomic numbers, names, symbols)

Output: Complete isotope database with:
- Atomic_Number
- Symbol  
- Element_Name
- Mass_Excess_keV
- Mass_Uncertainty_keV
- Half_Life
- Spin_Parity
- Year
- Decay_Modes
- Mass_Number
- Isomer
"""

import pandas as pd
import re

def extract_element_symbol(nuclide):
    """Extract element symbol from nuclide notation."""
    # Handle special cases first
    if nuclide == '1n':
        return 'n'  # neutron
    
    # Use regex to extract element symbol (handle isomer states)
    # Pattern: digits followed by element symbol (1-2 capital/lowercase letters)
    # followed by optional isomer indicators (i, m, n, p, etc.)
    match = re.match(r'^\d+([A-Z][a-z]?)', nuclide)
    if match:
        return match.group(1)
    
    return None

def extract_mass_number(nuclide):
    """Extract mass number from nuclide notation."""
    # Handle neutron case
    if nuclide == '1n':
        return 1
    
    # Extract leading digits
    match = re.match(r'^(\d+)', nuclide)
    if match:
        return int(match.group(1))
    
    return None

def main():
    print("Creating comprehensive isotope database...")
    
    # Read the nuclear data
    print("Reading NUBASE2020 nuclear data...")
    nuclear_df = pd.read_csv('data/nubase2020_complete_summary.csv')
    print(f"Found {len(nuclear_df)} nuclear entries")
    
    # Read the chemical elements data  
    print("Reading chemical elements data...")
    elements_df = pd.read_csv('data/chemical_elements_list.csv')
    print(f"Found {len(elements_df)} chemical elements")
    
    # Create a mapping from element symbol to atomic number and name
    element_map = {}
    for _, row in elements_df.iterrows():
        symbol = row['Symbol']
        element_map[symbol] = {
            'Atomic_Number': row['Atomic_Number'],
            'Element_Name': row['Element_Name']
        }
    
    # Add neutron as special case (atomic number 0)
    element_map['n'] = {
        'Atomic_Number': 0,
        'Element_Name': 'neutron'
    }
    
    # Map problematic isomer notations to correct elements
    # These appear to be unusual isomer states with extended notation
    isomer_corrections = {
        'Bj': 'B',   # Boron isomer j
        'Ci': 'C',   # Carbon isomer i  
        'Cj': 'C',   # Carbon isomer j
        'Fi': 'F',   # Fluorine isomer i
        'Km': 'K',   # Potassium isomer m
        'Nm': 'N',   # Nitrogen isomer m
        'Oi': 'O',   # Oxygen isomer i
        'Oj': 'O',   # Oxygen isomer j
        'Op': 'O',   # Oxygen isomer p
        'Pi': 'P',   # Phosphorus isomer i
        'Um': 'U',   # Uranium isomer m
        'Un': 'U'    # Uranium isomer n
    }
    
    # Add these corrections to element map
    for isomer_symbol, base_element in isomer_corrections.items():
        if base_element in element_map:
            element_map[isomer_symbol] = element_map[base_element]
    
    print("Processing nuclear data and matching with elements...")
    
    # Process each nuclear entry
    isotope_data = []
    unmatched_symbols = set()
    
    for _, row in nuclear_df.iterrows():
        nuclide = row['Nuclide']
        
        # Get element symbol from the Element column (more reliable)
        element_symbol = row['Element']
        mass_number = row['Mass_Number']
        
        if pd.isna(element_symbol) or pd.isna(mass_number):
            print(f"Warning: Missing element or mass number for nuclide {nuclide}")
            continue
            
        # Look up element information
        if element_symbol in element_map:
            element_info = element_map[element_symbol]
            atomic_number = element_info['Atomic_Number']
            element_name = element_info['Element_Name']
        else:
            unmatched_symbols.add(element_symbol)
            # Use placeholder values for unknown elements
            atomic_number = None
            element_name = f"Unknown_{element_symbol}"
        
        # Create isotope entry
        isotope_entry = {
            'Atomic_Number': atomic_number,
            'Symbol': element_symbol,
            'Element_Name': element_name,
            'Mass_Excess_keV': row['Mass_Excess_keV'],
            'Mass_Uncertainty_keV': row['Mass_Uncertainty_keV'],
            'Half_Life': row['Half_Life'],
            'Spin_Parity': row['Spin_Parity'],
            'Year': row['Year'],
            'Decay_Modes': row['Decay_Modes'],
            'Mass_Number': int(mass_number) if pd.notna(mass_number) else None,
            'Isomer': row['Isomer']
        }
        
        isotope_data.append(isotope_entry)
    
    # Report any unmatched symbols
    if unmatched_symbols:
        print(f"Warning: Found {len(unmatched_symbols)} unmatched element symbols:")
        for symbol in sorted(unmatched_symbols):
            print(f"  {symbol}")
    
    # Create DataFrame
    isotope_df = pd.DataFrame(isotope_data)
    
    # Sort by atomic number, then mass number, then isomer
    print("Sorting isotope database...")
    isotope_df = isotope_df.sort_values(['Atomic_Number', 'Mass_Number', 'Isomer'], na_position='first')
    
    # Save to CSV
    output_file = 'data/complete_isotope_database.csv'
    print(f"Saving complete isotope database to {output_file}...")
    isotope_df.to_csv(output_file, index=False)
    
    print(f"\nDatabase creation complete!")
    print(f"Total isotopes: {len(isotope_df)}")
    print(f"Elements represented: {isotope_df['Atomic_Number'].nunique()}")
    print(f"Mass number range: {isotope_df['Mass_Number'].min()} to {isotope_df['Mass_Number'].max()}")
    
    # Show summary by element
    print(f"\nIsotope count by element (top 10):")
    element_counts = isotope_df.groupby(['Atomic_Number', 'Element_Name']).size().sort_values(ascending=False)
    for (atomic_num, element_name), count in element_counts.head(10).items():
        atomic_num_str = str(int(atomic_num)) if pd.notna(atomic_num) else "N/A"
        print(f"  {atomic_num_str:3s} {element_name:12s}: {count:3d} isotopes")
    
    # Show first few entries
    print(f"\nFirst 10 entries:")
    print(isotope_df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()