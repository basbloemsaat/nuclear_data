#!/usr/bin/env python3
"""
Create individual JSON files for each isotope in data/isotopes/ directory.
Each file contains complete isotope data split by source (NUBASE2020 + Wikipedia).
Source metadata is stored in a separate sources.json file.
"""

import pandas as pd
import json
import os
from pathlib import Path

def sanitize_filename(name):
    """Sanitize a string to be safe for use as a filename."""
    name = name.replace('#', 'hash')
    name = name.replace('/', '_')
    name = name.replace('\\', '_')
    name = name.replace(':', '_')
    name = name.replace('*', '_')
    name = name.replace('?', '_')
    name = name.replace('"', '_')
    name = name.replace('<', '_')
    name = name.replace('>', '_')
    name = name.replace('|', '_')
    return name

def create_isotope_filename(z, a, symbol, isomer):
    """Create a standardized filename for an isotope."""
    isomer_str = f"_{isomer}" if pd.notna(isomer) and isomer != '' else ""
    return f"{z:03d}_{a:03d}_{symbol}{isomer_str}.json"

def convert_to_serializable(obj):
    """Convert pandas/numpy types to JSON serializable types."""
    if pd.isna(obj):
        return None
    elif hasattr(obj, 'item'):  # numpy types
        return obj.item()
    else:
        return obj

def create_combined_isotope_data(isotope_row, element_row, idx, total):
    """Create combined isotope data structure with sources separated."""
    z = int(isotope_row['Atomic_Number']) if pd.notna(isotope_row['Atomic_Number']) else 0
    a = int(isotope_row['Mass_Number']) if pd.notna(isotope_row['Mass_Number']) else 0
    symbol = isotope_row['Symbol']
    element_name = isotope_row['Element_Name']
    isomer = isotope_row['Isomer']
    
    # Base identification (common to both sources)
    isotope_data = {
        "identification": {
            "atomic_number": z,
            "mass_number": a,
            "symbol": symbol,
            "element_name": element_name,
            "isomer_state": convert_to_serializable(isomer),
            "isotope_notation": f"{a}{symbol}" + (f"{isomer}" if pd.notna(isomer) and isomer != '' else "")
        },
        "sources": {
            "nubase2020": {
                "nuclear_properties": {
                    "mass_excess_keV": convert_to_serializable(isotope_row['Mass_Excess_keV']),
                    "mass_uncertainty_keV": convert_to_serializable(isotope_row['Mass_Uncertainty_keV']),
                    "half_life": convert_to_serializable(isotope_row['Half_Life']),
                    "spin_parity": convert_to_serializable(isotope_row['Spin_Parity']),
                    "discovery_year": convert_to_serializable(isotope_row['Year']),
                    "decay_modes": convert_to_serializable(isotope_row['Decay_Modes'])
                }
            },
            "wikipedia": None  # Will be filled if element data exists
        },
        "metadata": {
            "sources_available": ["nubase2020"],
            "database_entry_index": idx + 1,
            "total_entries": total
        }
    }
    
    # Add Wikipedia element data if available
    if element_row is not None:
        isotope_data["sources"]["wikipedia"] = {
            "chemical_properties": {
                "name_origin": convert_to_serializable(element_row['Name_Origin']),
                "group": convert_to_serializable(element_row['Group']),
                "period": int(element_row['Period']) if pd.notna(element_row['Period']) else None,
                "block": convert_to_serializable(element_row['Block'])
            },
            "physical_properties": {
                "atomic_weight": convert_to_serializable(element_row['Atomic_Weight']),
                "density": convert_to_serializable(element_row['Density']),
                "melting_point": convert_to_serializable(element_row['Melting_Point']),
                "boiling_point": convert_to_serializable(element_row['Boiling_Point']),
                "phase": convert_to_serializable(element_row['Phase'])
            },
            "classification": {
                "origin": convert_to_serializable(element_row['Origin'])
            }
        }
        isotope_data["metadata"]["sources_available"].append("wikipedia")
    
    return isotope_data

def create_sources_metadata():
    """Create the centralized sources metadata."""
    return {
        "sources": {
            "nubase2020": {
                "source": "NUBASE2020",
                "description": "Nuclear physics properties from NUBASE2020 evaluation - complete Table I",
                "source_pages": "NUBASE2020 pages 21-181",
                "extraction_date": "2025-11-15",
                "data_fields": [
                    "mass_excess_keV", "mass_uncertainty_keV", "half_life",
                    "spin_parity", "discovery_year", "decay_modes"
                ],
                "coverage": "All known isotopes from neutron to superheavy elements",
                "reference": "NUBASE2020 evaluation of nuclear and decay properties"
            },
            "wikipedia": {
                "source": "Wikipedia",
                "description": "Chemical element properties from Wikipedia List of Chemical Elements",
                "source_url": "https://en.wikipedia.org/wiki/List_of_chemical_elements",
                "extraction_date": "2025-11-15",
                "data_fields": [
                    "name_origin", "group", "period", "block", "atomic_weight",
                    "density", "melting_point", "boiling_point", "phase", "origin"
                ],
                "coverage": "All 118 chemical elements H to Og",
                "reference": "Wikipedia List of Chemical Elements"
            }
        },
        "metadata": {
            "file_purpose": "Centralized source metadata for isotope database",
            "creation_date": "2025-11-15",
            "version": "1.0",
            "note": "This file contains metadata for all data sources used in the isotope database. Individual isotope files reference these sources by key."
        }
    }

def main():
    print("Creating combined isotope files with centralized source metadata...")
    
    # Create output directory
    output_dir = Path('data/isotopes')
    # Remove existing files if directory exists
    if output_dir.exists():
        print(f"Removing existing files in {output_dir}")
        for file in output_dir.glob('*.json'):
            file.unlink()
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Read the databases
    print("Reading databases...")
    isotope_df = pd.read_csv('data/complete_isotope_database.csv')
    elements_df = pd.read_csv('data/chemical_elements_list.csv')
    
    print(f"Processing {len(isotope_df)} isotopes")
    print(f"Available element data for {len(elements_df)} elements")
    
    # Create element lookup dictionary
    element_lookup = {}
    for _, row in elements_df.iterrows():
        element_lookup[row['Symbol']] = row
    
    # Track statistics
    created_files = 0
    failed_files = 0
    elements_matched = 0
    elements_missing = 0
    
    for idx, isotope_row in isotope_df.iterrows():
        try:
            z = int(isotope_row['Atomic_Number']) if pd.notna(isotope_row['Atomic_Number']) else 0
            a = int(isotope_row['Mass_Number']) if pd.notna(isotope_row['Mass_Number']) else 0
            symbol = isotope_row['Symbol']
            isomer = isotope_row['Isomer']
            
            # Look up element data
            element_row = element_lookup.get(symbol)
            if element_row is not None:
                elements_matched += 1
            else:
                elements_missing += 1
            
            # Create combined data structure
            isotope_data = create_combined_isotope_data(isotope_row, element_row, idx, len(isotope_df))
            
            # Create filename and save
            filename = create_isotope_filename(z, a, symbol, isomer)
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(isotope_data, f, indent=2, ensure_ascii=False)
            
            created_files += 1
            
            # Progress indicator
            if created_files % 200 == 0:
                print(f"  Created {created_files} files...")
                
        except Exception as e:
            print(f"Failed to create file for isotope {idx+1}: {e}")
            failed_files += 1
    
    # Create centralized sources metadata file
    print(f"\nCreating centralized sources metadata file...")
    sources_metadata = create_sources_metadata()
    with open(output_dir / 'sources.json', 'w', encoding='utf-8') as f:
        json.dump(sources_metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\nFile creation complete!")
    print(f"Successfully created: {created_files} isotope files")
    print(f"Failed: {failed_files} files")
    print(f"Elements matched: {elements_matched}")
    print(f"Elements missing: {elements_missing}")
    
    # Show file size statistics
    isotope_files = [f for f in os.listdir(output_dir) if f.endswith('.json') and f not in ['sources.json', 'index.json']]
    total_isotope_size = sum(os.path.getsize(output_dir / f) for f in isotope_files)
    avg_size = total_isotope_size / len(isotope_files) if isotope_files else 0
    sources_size = os.path.getsize(output_dir / 'sources.json')
    
    print(f"\nStorage statistics:")
    print(f"Isotope files: {total_isotope_size / 1024:.1f} KB ({len(isotope_files)} files)")
    print(f"Sources metadata: {sources_size / 1024:.1f} KB (1 file)")
    print(f"Total: {(total_isotope_size + sources_size) / 1024:.1f} KB")
    print(f"Average isotope file size: {avg_size:.0f} bytes")
    
    # Show sample filenames
    print(f"\nSample files created:")
    sample_files = sorted(isotope_files)[:10]
    for filename in sample_files:
        print(f"  {filename}")
    
    if len(sample_files) < len(isotope_files):
        print(f"  ... and {len(isotope_files) - len(sample_files)} more isotope files")
    print(f"  sources.json")
    
    # Show sample content from first file
    if isotope_files:
        sample_file = output_dir / sorted(isotope_files)[0]
        print(f"\nSample content from {sample_file.name}:")
        with open(sample_file, 'r') as f:
            sample_content = json.load(f)
        
        # Show structure overview
        print("File structure:")
        print(f"  - identification: {list(sample_content['identification'].keys())}")
        print(f"  - sources:")
        for source, data in sample_content['sources'].items():
            if data is not None:
                print(f"    - {source}: {list(data.keys())}")
            else:
                print(f"    - {source}: None")
        print(f"  - metadata: {list(sample_content['metadata'].keys())}")
    
    # Create summary index file
    print(f"\nCreating summary index file...")
    summary = {
        "database_info": {
            "title": "Combined Nuclear Isotope Database",
            "description": "Individual isotope files combining NUBASE2020 nuclear data with Wikipedia chemical element properties",
            "total_isotopes": created_files,
            "creation_date": "2025-11-15"
        },
        "file_structure": {
            "isotope_files": {
                "naming_convention": "ZZZ_AAA_Symbol_isomer.json",
                "total_files": created_files,
                "average_file_size_bytes": avg_size,
                "total_size_kb": total_isotope_size / 1024
            },
            "metadata_files": {
                "sources.json": "Centralized source metadata for all data sources",
                "index.json": "Database summary and file structure information"
            }
        },
        "data_coverage": {
            "atomic_number_range": f"0-{isotope_df['Atomic_Number'].max():.0f}",
            "mass_number_range": f"{isotope_df['Mass_Number'].min():.0f}-{isotope_df['Mass_Number'].max():.0f}",
            "elements_with_chemical_data": elements_matched,
            "elements_nuclear_only": elements_missing
        },
        "usage_note": "Source metadata is centralized in sources.json. Individual isotope files reference sources by key ('nubase2020', 'wikipedia')."
    }
    
    with open(output_dir / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("Summary index created: data/isotopes/index.json")
    print("Sources metadata created: data/isotopes/sources.json")

if __name__ == "__main__":
    main()