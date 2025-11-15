#!/usr/bin/env python3
"""
Create a comprehensive summary of the extracted NUBASE2020 Table I data
"""

import pandas as pd
import numpy as np

def analyze_extracted_data():
    """Analyze the extracted NUBASE2020 Table I data"""
    
    # Read the extracted data
    df = pd.read_csv('/home/bas/src/nuclear_data/data/nubase2020_table_i_complete.csv')
    
    print("="*80)
    print("NUBASE2020 TABLE I EXTRACTION SUMMARY")
    print("="*80)
    
    print(f"Total nuclear entries extracted: {len(df)}")
    
    # Analyze by element
    print("\nEntries by element:")
    elements = df['Nuclide'].str.extract(r'(\d+)([A-Z][a-z]?)')[1].value_counts().head(20)
    print(elements)
    
    # Mass range
    print(f"\nMass number range:")
    mass_numbers = df['Nuclide'].str.extract(r'(\d+)')[0].astype(int)
    print(f"From A = {mass_numbers.min()} to A = {mass_numbers.max()}")
    
    # Show some examples of different types of entries
    print("\nExamples of different entry types:")
    print("\n1. Stable isotopes:")
    stable = df[df['Half_Life'] == 'STABLE'].head(5)
    for _, row in stable.iterrows():
        print(f"   {row['Nuclide']}: Mass excess = {row['Mass_Excess_keV']} keV")
    
    print("\n2. Radioactive isotopes with decay modes:")
    radioactive = df[df['Decay_Modes'].str.contains('β', na=False)].head(5)
    for _, row in radioactive.iterrows():
        print(f"   {row['Nuclide']}: {row['Decay_Modes']}")
    
    print("\n3. Entries with half-lives:")
    with_halflife = df[df['Half_Life'].str.contains('s|m|h|d|y', na=False)].head(5)
    for _, row in with_halflife.iterrows():
        print(f"   {row['Nuclide']}: {row['Half_Life']}")
    
    # Check for different isotopes of common elements
    print("\n4. Hydrogen isotopes:")
    hydrogen = df[df['Nuclide'].str.contains(r'^\d+H')]
    for _, row in hydrogen.iterrows():
        print(f"   {row['Nuclide']}: Mass excess = {row['Mass_Excess_keV']} keV, Half-life = {row['Half_Life']}")
    
    print("\n5. Helium isotopes:")
    helium = df[df['Nuclide'].str.contains(r'^\d+He')]
    for _, row in helium.iterrows():
        print(f"   {row['Nuclide']}: Mass excess = {row['Mass_Excess_keV']} keV, Half-life = {row['Half_Life']}")
    
    # Save a cleaned version
    print("\nSaving cleaned summary...")
    
    # Create a cleaned summary version
    summary_df = df[['Nuclide', 'Mass_Excess_keV', 'Mass_Uncertainty_keV', 
                    'Half_Life', 'Spin_Parity', 'Year', 'Decay_Modes']].copy()
    
    # Clean up the data
    summary_df['Mass_Number'] = summary_df['Nuclide'].str.extract(r'(\d+)')[0].astype(int)
    # Handle both uppercase and lowercase elements (e.g., 1n for neutron)
    summary_df['Element'] = summary_df['Nuclide'].str.extract(r'\d+([A-Za-z][a-z]?)')[0]
    summary_df['Isomer'] = summary_df['Nuclide'].str.extract(r'[A-Za-z][a-z]?([imn-zx]+)')[0]
    
    # Sort by mass number, but put neutron (1n) first
    summary_df = summary_df.sort_values(['Mass_Number', 'Element', 'Isomer'])
    
    # Move neutron to the very beginning
    neutron_mask = summary_df['Nuclide'] == '1n'
    neutron_row = summary_df[neutron_mask]
    other_rows = summary_df[~neutron_mask]
    summary_df = pd.concat([neutron_row, other_rows], ignore_index=True)
    
    # Save the cleaned summary
    output_file = "/home/bas/src/nuclear_data/data/nubase2020_complete_summary.csv"
    summary_df.to_csv(output_file, index=False)
    print(f"Saved cleaned summary to: {output_file}")
    
    # Create a separate file with just the essential data
    essential_df = summary_df[['Mass_Number', 'Element', 'Nuclide', 'Mass_Excess_keV', 
                              'Half_Life', 'Decay_Modes']].copy()
    essential_file = "/home/bas/src/nuclear_data/data/nubase2020_complete_essential.csv"
    essential_df.to_csv(essential_file, index=False)
    print(f"Saved essential data to: {essential_file}")
    
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    print("\nFiles created:")
    print("1. nubase2020_table_i_extracted.csv - Raw extracted data")
    print("2. nubase2020_table_i_summary.csv - Cleaned and sorted data") 
    print("3. nubase2020_table_i_essential.csv - Essential columns only")
    print("\nThis represents Table I from NUBASE2020, containing nuclear and decay")
    print("properties for the ground states and excited isomeric states of nuclei.")

if __name__ == "__main__":
    analyze_extracted_data()