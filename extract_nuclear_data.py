#!/usr/bin/env python3
"""
Extract Table I entries directly from the extracted text using a simpler approach
"""

import pandas as pd
import re
from pathlib import Path

def extract_nuclear_data_entries(text_file):
    """Extract nuclear data entries from the text file"""
    
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for lines that contain nuclear data
    # These typically have the pattern: number + element + space + number (mass excess)
    nuclear_entries = []
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, comment lines, and headers
        if not line or line.startswith('∗') or line.startswith('=') or 'Page' in line:
            continue
            
        # Look for nuclear data pattern: starts with isotope name (number + letters)
        # Examples: 1n, 1H, 2H, 3H, 8He, etc.
        # Updated to include lowercase 'n' for neutron
        match = re.match(r'^(\d+[A-Za-z][a-z]?[imn-zx]*)\s+(.+)', line)
        
        if match:
            nuclide = match.group(1)
            rest_of_line = match.group(2)
            
            # Parse the rest of the line
            parts = rest_of_line.split()
            
            if len(parts) >= 3:  # Minimum: mass_excess, uncertainty, half-life
                try:
                    mass_excess = parts[0]
                    
                    # Skip lines that don't have proper mass excess values
                    if not (mass_excess.replace('-', '').replace('.', '').replace('#', '').isdigit()):
                        continue
                    
                    nuclear_entries.append({
                        'Nuclide': nuclide,
                        'Original_Line': line
                    })
                    
                except:
                    continue
    
    print(f"Found {len(nuclear_entries)} potential nuclear data entries")
    
    # Show first few entries
    for i, entry in enumerate(nuclear_entries[:10]):
        print(f"{i+1:2d}: {entry['Nuclide']} - {entry['Original_Line'][:80]}...")
    
    return nuclear_entries

def parse_nubase_line(line):
    """Parse a single NUBASE data line"""
    parts = line.split()
    
    if len(parts) < 5:
        return None
    
    try:
        nuclide = parts[0]
        mass_excess = parts[1]
        uncertainty = parts[2] if len(parts) > 2 else ''
        
        # Find half-life (contains time units or special values)
        half_life = ''
        time_patterns = [
            r'\d+\.?\d*\s*(ys|zs|as|fs|ps|ns|µs|ms|s|m|h|d|y|ky|My|Gy)',
            r'STABLE',
            r'p-unstable'
        ]
        
        for part in parts:
            for pattern in time_patterns:
                if re.search(pattern, part):
                    half_life = part
                    break
            if half_life:
                break
        
        # Find spin/parity
        spin_parity = ''
        for part in parts:
            if re.match(r'.*[/+\-](\*)?$', part) and not '=' in part:
                spin_parity = part
                break
        
        # Find year
        year = ''
        for part in parts:
            if re.match(r'^\d{2,4}$', part):
                year = part
                break
        
        # Find decay modes
        decay_modes = []
        for part in parts:
            if '=' in part and any(mode in part for mode in ['α', 'β', 'p', 'n', 'ε', 'IT', 'SF', 'IS']):
                decay_modes.append(part)
        
        return {
            'Nuclide': nuclide,
            'Mass_Excess_keV': mass_excess,
            'Mass_Uncertainty_keV': uncertainty,
            'Half_Life': half_life,
            'Spin_Parity': spin_parity,
            'Year': year,
            'Decay_Modes': ';'.join(decay_modes),
            'Original_Line': line.strip()
        }
        
    except Exception as e:
        print(f"Error parsing line: {line[:50]}... Error: {e}")
        return None

if __name__ == "__main__":
    text_file = "/home/bas/src/nuclear_data/data/complete_table_text.txt"
    
    print("Extracting nuclear data entries from NUBASE2020...")
    entries = extract_nuclear_data_entries(text_file)
    
    if entries:
        # Parse each entry
        parsed_entries = []
        for entry in entries:
            parsed = parse_nubase_line(entry['Original_Line'])
            if parsed:
                parsed_entries.append(parsed)
        
        if parsed_entries:
            # Save to CSV
            df = pd.DataFrame(parsed_entries)
            output_file = "/home/bas/src/nuclear_data/data/nubase2020_table_i_complete.csv"
            df.to_csv(output_file, index=False)
            
            print(f"\nSuccessfully extracted {len(parsed_entries)} nuclear data entries")
            print(f"Saved to: {output_file}")
            
            # Display first few entries
            print("\nFirst 10 extracted entries:")
            print(df[['Nuclide', 'Mass_Excess_keV', 'Half_Life', 'Spin_Parity', 'Year']].head(10).to_string())
        else:
            print("No entries could be parsed successfully")
    else:
        print("No nuclear data entries found")