#!/usr/bin/env python3
"""
Split isotope data by source: NUBASE2020 nuclear data vs Wikipedia chemical elements data.
Creates separate JSON files organized by data source.
"""

import pandas as pd
import json
import os
from pathlib import Path

def create_nubase_isotope_data(row, idx, total):
    """Create isotope data structure focused on NUBASE2020 nuclear physics data."""
    z = int(row['Atomic_Number']) if pd.notna(row['Atomic_Number']) else 0
    a = int(row['Mass_Number']) if pd.notna(row['Mass_Number']) else 0
    symbol = row['Symbol']
    isomer = row['Isomer']
    
    return {
        "identification": {
            "atomic_number": z,
            "mass_number": a,
            "symbol": symbol,
            "isomer_state": isomer if pd.notna(isomer) and isomer != '' else None,
            "isotope_notation": f"{a}{symbol}" + (f"{isomer}" if pd.notna(isomer) and isomer != '' else "")
        },
        "nuclear_data": {
            "mass_excess_keV": row['Mass_Excess_keV'] if pd.notna(row['Mass_Excess_keV']) else None,
            "mass_uncertainty_keV": row['Mass_Uncertainty_keV'] if pd.notna(row['Mass_Uncertainty_keV']) else None,
            "half_life": row['Half_Life'] if pd.notna(row['Half_Life']) else None,
            "spin_parity": row['Spin_Parity'] if pd.notna(row['Spin_Parity']) else None,
            "discovery_year": row['Year'] if pd.notna(row['Year']) else None,
            "decay_modes": row['Decay_Modes'] if pd.notna(row['Decay_Modes']) else None
        },
        "source_metadata": {
            "source": "NUBASE2020",
            "description": "Nuclear physics properties from NUBASE2020 evaluation",
            "data_extraction_date": "2025-11-15",
            "entry_index": idx + 1,
            "total_entries": total
        }
    }

def create_chemical_element_data(elements_df):
    """Create chemical elements data structure from Wikipedia data."""
    elements_data = []
    
    for _, row in elements_df.iterrows():
        element_data = {
            "identification": {
                "atomic_number": int(row['Atomic_Number']),
                "symbol": row['Symbol'],
                "element_name": row['Element_Name']
            },
            "chemical_properties": {
                "name_origin": row['Name_Origin'] if pd.notna(row['Name_Origin']) else None,
                "group": row['Group'] if pd.notna(row['Group']) else None,
                "period": int(row['Period']) if pd.notna(row['Period']) else None,
                "block": row['Block'] if pd.notna(row['Block']) else None
            },
            "physical_properties": {
                "atomic_weight": row['Atomic_Weight'] if pd.notna(row['Atomic_Weight']) else None,
                "density": row['Density'] if pd.notna(row['Density']) else None,
                "melting_point": row['Melting_Point'] if pd.notna(row['Melting_Point']) else None,
                "boiling_point": row['Boiling_Point'] if pd.notna(row['Boiling_Point']) else None,
                "phase": row['Phase'] if pd.notna(row['Phase']) else None
            },
            "classification": {
                "origin": row['Origin'] if pd.notna(row['Origin']) else None
            },
            "source_metadata": {
                "source": "Wikipedia",
                "description": "Chemical element properties from Wikipedia List of Chemical Elements",
                "data_extraction_date": "2025-11-15"
            }
        }
        elements_data.append(element_data)
    
    return elements_data

def create_isotope_filename(z, a, symbol, isomer):
    """Create standardized filename for isotope."""
    isomer_str = f"_{isomer}" if pd.notna(isomer) and isomer != '' else ""
    return f"{z:03d}_{a:03d}_{symbol}{isomer_str}.json"

def create_element_filename(z, symbol):
    """Create standardized filename for element."""
    return f"{z:03d}_{symbol}.json"

def main():
    print("Splitting isotope data by source...")
    
    # Create output directories
    nubase_dir = Path('data/sources/nubase2020')
    wikipedia_dir = Path('data/sources/wikipedia')
    nubase_dir.mkdir(parents=True, exist_ok=True)
    wikipedia_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"NUBASE2020 directory: {nubase_dir}")
    print(f"Wikipedia directory: {wikipedia_dir}")
    
    # Read the databases
    isotope_df = pd.read_csv('data/complete_isotope_database.csv')
    elements_df = pd.read_csv('data/chemical_elements_list.csv')
    
    print(f"Processing {len(isotope_df)} isotopes from NUBASE2020")
    print(f"Processing {len(elements_df)} elements from Wikipedia")
    
    # Process NUBASE2020 nuclear data
    print("\nCreating NUBASE2020 nuclear data files...")
    nubase_created = 0
    
    for idx, row in isotope_df.iterrows():
        try:
            z = int(row['Atomic_Number']) if pd.notna(row['Atomic_Number']) else 0
            a = int(row['Mass_Number']) if pd.notna(row['Mass_Number']) else 0
            symbol = row['Symbol']
            isomer = row['Isomer']
            
            # Create NUBASE2020 data structure
            nubase_data = create_nubase_isotope_data(row, idx, len(isotope_df))
            
            # Save NUBASE2020 file
            filename = create_isotope_filename(z, a, symbol, isomer)
            filepath = nubase_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(nubase_data, f, indent=2, ensure_ascii=False)
            
            nubase_created += 1
            
            if nubase_created % 200 == 0:
                print(f"  Created {nubase_created} NUBASE2020 files...")
                
        except Exception as e:
            print(f"Failed to create NUBASE2020 file for isotope {idx+1}: {e}")
    
    # Process Wikipedia chemical elements data
    print(f"\nCreating Wikipedia chemical elements files...")
    wikipedia_created = 0
    
    for _, row in elements_df.iterrows():
        try:
            z = int(row['Atomic_Number'])
            symbol = row['Symbol']
            
            # Create element data structure
            element_data = {
                "identification": {
                    "atomic_number": z,
                    "symbol": symbol,
                    "element_name": row['Element_Name']
                },
                "chemical_properties": {
                    "name_origin": row['Name_Origin'] if pd.notna(row['Name_Origin']) else None,
                    "group": row['Group'] if pd.notna(row['Group']) else None,
                    "period": int(row['Period']) if pd.notna(row['Period']) else None,
                    "block": row['Block'] if pd.notna(row['Block']) else None
                },
                "physical_properties": {
                    "atomic_weight": row['Atomic_Weight'] if pd.notna(row['Atomic_Weight']) else None,
                    "density": row['Density'] if pd.notna(row['Density']) else None,
                    "melting_point": row['Melting_Point'] if pd.notna(row['Melting_Point']) else None,
                    "boiling_point": row['Boiling_Point'] if pd.notna(row['Boiling_Point']) else None,
                    "phase": row['Phase'] if pd.notna(row['Phase']) else None
                },
                "classification": {
                    "origin": row['Origin'] if pd.notna(row['Origin']) else None
                },
                "source_metadata": {
                    "source": "Wikipedia",
                    "description": "Chemical element properties from Wikipedia List of Chemical Elements",
                    "data_extraction_date": "2025-11-15",
                    "entry_index": wikipedia_created + 1,
                    "total_entries": len(elements_df)
                }
            }
            
            # Save Wikipedia file
            filename = create_element_filename(z, symbol)
            filepath = wikipedia_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(element_data, f, indent=2, ensure_ascii=False)
            
            wikipedia_created += 1
            
        except Exception as e:
            print(f"Failed to create Wikipedia file for element {row['Symbol']}: {e}")
    
    # Create summary index files
    print(f"\nCreating summary index files...")
    
    # NUBASE2020 summary
    nubase_summary = {
        "source": "NUBASE2020",
        "description": "Nuclear physics data from NUBASE2020 evaluation - complete Table I",
        "total_isotopes": nubase_created,
        "data_range": {
            "atomic_numbers": f"0-{isotope_df['Atomic_Number'].max():.0f}",
            "mass_numbers": f"{isotope_df['Mass_Number'].min():.0f}-{isotope_df['Mass_Number'].max():.0f}"
        },
        "data_fields": [
            "mass_excess_keV",
            "mass_uncertainty_keV", 
            "half_life",
            "spin_parity",
            "discovery_year",
            "decay_modes"
        ],
        "extraction_date": "2025-11-15",
        "source_pages": "NUBASE2020 pages 21-181"
    }
    
    with open(nubase_dir / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(nubase_summary, f, indent=2, ensure_ascii=False)
    
    # Wikipedia summary
    wikipedia_summary = {
        "source": "Wikipedia",
        "description": "Chemical element properties from Wikipedia List of Chemical Elements",
        "total_elements": wikipedia_created,
        "data_range": {
            "atomic_numbers": f"1-{elements_df['Atomic_Number'].max()}"
        },
        "data_fields": [
            "name_origin",
            "group",
            "period", 
            "block",
            "atomic_weight",
            "density",
            "melting_point",
            "boiling_point",
            "phase",
            "origin"
        ],
        "extraction_date": "2025-11-15",
        "source_url": "https://en.wikipedia.org/wiki/List_of_chemical_elements"
    }
    
    with open(wikipedia_dir / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(wikipedia_summary, f, indent=2, ensure_ascii=False)
    
    # Overall summary
    print(f"\nData split complete!")
    print(f"NUBASE2020 files created: {nubase_created}")
    print(f"Wikipedia files created: {wikipedia_created}")
    
    # Show storage statistics
    nubase_size = sum(os.path.getsize(nubase_dir / f) for f in os.listdir(nubase_dir) if f.endswith('.json'))
    wikipedia_size = sum(os.path.getsize(wikipedia_dir / f) for f in os.listdir(wikipedia_dir) if f.endswith('.json'))
    
    print(f"\nStorage statistics:")
    print(f"NUBASE2020 data: {nubase_size / 1024:.1f} KB ({nubase_created} files)")
    print(f"Wikipedia data: {wikipedia_size / 1024:.1f} KB ({wikipedia_created} files)")
    print(f"Total: {(nubase_size + wikipedia_size) / 1024:.1f} KB")
    
    # Show sample files
    print(f"\nSample NUBASE2020 files:")
    nubase_files = sorted([f for f in os.listdir(nubase_dir) if f.endswith('.json') and f != 'index.json'])[:5]
    for f in nubase_files:
        print(f"  {f}")
    
    print(f"\nSample Wikipedia files:")
    wikipedia_files = sorted([f for f in os.listdir(wikipedia_dir) if f.endswith('.json') and f != 'index.json'])[:5]
    for f in wikipedia_files:
        print(f"  {f}")

if __name__ == "__main__":
    main()