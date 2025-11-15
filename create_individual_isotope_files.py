#!/usr/bin/env python3
"""
Create individual JSON files for each isotope in data/isotopes/ directory.
Each file contains complete isotope data including all nuclear properties.
"""

import pandas as pd
import json
import os
from pathlib import Path

def sanitize_filename(name):
    """Sanitize a string to be safe for use as a filename."""
    # Replace problematic characters
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
    elif isinstance(obj, (pd.Int64Dtype, pd.Float64Dtype)):
        return None if pd.isna(obj) else obj
    elif hasattr(obj, 'item'):  # numpy types
        return obj.item()
    else:
        return obj

def main():
    print("Creating individual JSON files for each isotope...")
    
    # Create output directory
    output_dir = Path('data/isotopes')
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Read the complete isotope database
    df = pd.read_csv('data/complete_isotope_database.csv')
    print(f"Processing {len(df)} isotopes")
    
    # Track statistics
    created_files = 0
    failed_files = 0
    
    for idx, row in df.iterrows():
        try:
            # Extract basic identification
            z = int(row['Atomic_Number']) if pd.notna(row['Atomic_Number']) else 0
            a = int(row['Mass_Number']) if pd.notna(row['Mass_Number']) else 0
            symbol = row['Symbol']
            element_name = row['Element_Name']
            isomer = row['Isomer']
            
            # Create complete isotope data structure
            isotope_data = {
                "identification": {
                    "atomic_number": z,
                    "mass_number": a,
                    "symbol": symbol,
                    "element_name": element_name,
                    "isomer_state": convert_to_serializable(isomer),
                    "isotope_notation": f"{a}{symbol}" + (f"{isomer}" if pd.notna(isomer) and isomer != '' else "")
                },
                "nuclear_properties": {
                    "mass_excess_keV": convert_to_serializable(row['Mass_Excess_keV']),
                    "mass_uncertainty_keV": convert_to_serializable(row['Mass_Uncertainty_keV']),
                    "half_life": convert_to_serializable(row['Half_Life']),
                    "spin_parity": convert_to_serializable(row['Spin_Parity']),
                    "discovery_year": convert_to_serializable(row['Year']),
                    "decay_modes": convert_to_serializable(row['Decay_Modes'])
                },
                "metadata": {
                    "source_database": "NUBASE2020 + Wikipedia Chemical Elements",
                    "data_extraction_date": "2025-11-15",
                    "database_entry_index": idx + 1,
                    "total_entries": len(df)
                }
            }
            
            # Create filename
            filename = create_isotope_filename(z, a, symbol, isomer)
            filepath = output_dir / filename
            
            # Write JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(isotope_data, f, indent=2, ensure_ascii=False)
            
            created_files += 1
            
            # Progress indicator
            if created_files % 100 == 0:
                print(f"  Created {created_files} files...")
                
        except Exception as e:
            print(f"Failed to create file for isotope {idx+1}: {e}")
            failed_files += 1
    
    print(f"\nFile creation complete!")
    print(f"Successfully created: {created_files} files")
    print(f"Failed: {failed_files} files")
    print(f"Total processed: {len(df)} isotopes")
    
    # Show some example filenames
    print(f"\nExample files created:")
    example_files = sorted(os.listdir(output_dir))[:10]
    for filename in example_files:
        print(f"  {filename}")
    
    if len(example_files) < len(os.listdir(output_dir)):
        print(f"  ... and {len(os.listdir(output_dir)) - len(example_files)} more files")
    
    # Show file size statistics
    total_size = sum(os.path.getsize(output_dir / f) for f in os.listdir(output_dir))
    avg_size = total_size / len(os.listdir(output_dir)) if os.listdir(output_dir) else 0
    print(f"\nStorage statistics:")
    print(f"Total size: {total_size / 1024:.1f} KB")
    print(f"Average file size: {avg_size:.0f} bytes")
    
    # Show sample content from first file
    if os.listdir(output_dir):
        sample_file = output_dir / sorted(os.listdir(output_dir))[0]
        print(f"\nSample content from {sample_file.name}:")
        with open(sample_file, 'r') as f:
            sample_content = json.load(f)
        print(json.dumps(sample_content, indent=2)[:500] + "...")

if __name__ == "__main__":
    main()