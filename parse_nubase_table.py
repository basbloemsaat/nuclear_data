#!/usr/bin/env python3
"""
Parse and extract Table I from the extracted NUBASE2020 text
"""

import pandas as pd
import re
from pathlib import Path

def parse_nubase_table(text_file):
    """Parse the NUBASE2020 Table I from extracted text"""
    
    # Read the extracted text
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the start of the actual table data
    table_start = content.find("TableI.TheNUBASE2020table(ExplanationofTableonpage030001-16)")
    if table_start == -1:
        print("Could not find the start of Table I")
        return None
    
    # Extract the table section
    table_section = content[table_start:]
    
    # Split into lines and process
    lines = table_section.split('\n')
    
    # Find data lines (skip headers and explanations)
    data_lines = []
    in_data_section = False
    
    for line in lines:
        # Skip empty lines and headers
        if not line.strip():
            continue
            
        # Look for the start of actual data (after column headers)
        if 'Nuclide' in line and 'Massexcess' in line and '(keV)' in line:
            in_data_section = True
            continue
            
        if not in_data_section:
            continue
            
        # Skip comment lines starting with *
        if line.strip().startswith('∗'):
            continue
            
        # Look for nuclear data lines
        # Nuclear data typically starts with mass number + element symbol
        if re.match(r'^\d+[A-Z][a-z]?[imn-zx]*\s', line):
            data_lines.append(line)
    
    print(f"Found {len(data_lines)} data lines")
    
    # Parse each data line
    parsed_data = []
    
    for line in data_lines:
        try:
            # Split the line carefully considering the complex format
            parts = line.split()
            if len(parts) < 7:  # Skip incomplete lines
                continue
                
            nuclide = parts[0]
            mass_excess = parts[1]
            mass_uncertainty = parts[2] if parts[2].replace('.', '').replace('-', '').replace('#', '').isdigit() else ''
            
            # Find half-life (look for time units)
            time_units = ['s', 'ms', 'µs', 'ns', 'ps', 'fs', 'as', 'zs', 'ys',
                         'm', 'h', 'd', 'y', 'ky', 'My', 'Gy', 'Ty', 'Py', 'Ey', 'Zy', 'Yy',
                         'STABLE', 'p-unstable']
            
            half_life = ''
            half_life_uncertainty = ''
            
            # Look for half-life in the line
            for i, part in enumerate(parts):
                for unit in time_units:
                    if unit in part:
                        half_life = part
                        if i > 0 and parts[i-1].replace('.', '').isdigit():
                            half_life = parts[i-1] + ' ' + part
                        break
                if half_life:
                    break
            
            # Extract spin/parity (look for patterns like 1/2+, 0+, etc.)
            spin_parity = ''
            for part in parts:
                if re.match(r'.*[+-](\*)?$', part) or part in ['high', 'low', 'am']:
                    spin_parity = part
                    break
            
            # Extract year (4-digit number or 2-digit year)
            year = ''
            for part in parts:
                if re.match(r'^\d{2,4}$', part):
                    year = part
                    break
            
            # Find decay modes (look for patterns like β−=100, α=100, etc.)
            decay_info = []
            decay_started = False
            for part in parts:
                if '=' in part and any(mode in part for mode in ['α', 'β', 'p', 'n', 'ε', 'IT', 'SF', 'IS']):
                    decay_started = True
                    decay_info.append(part)
                elif decay_started and ('+' in part or '-' in part or '?' in part):
                    decay_info.append(part)
            
            decay_modes = ';'.join(decay_info) if decay_info else ''
            
            parsed_entry = {
                'Nuclide': nuclide,
                'Mass_Excess_keV': mass_excess,
                'Mass_Uncertainty_keV': mass_uncertainty,
                'Half_Life': half_life,
                'Spin_Parity': spin_parity,
                'Year_Discovery': year,
                'Decay_Modes': decay_modes,
                'Original_Line': line.strip()
            }
            
            parsed_data.append(parsed_entry)
            
        except Exception as e:
            print(f"Error parsing line: {line[:50]}... Error: {e}")
            continue
    
    return parsed_data

def save_to_csv(data, output_file):
    """Save parsed data to CSV"""
    if not data:
        print("No data to save")
        return
        
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Saved {len(data)} entries to {output_file}")
    
    # Show first few entries
    print("\nFirst 10 entries:")
    print(df.head(10).to_string())

if __name__ == "__main__":
    text_file = "/home/bas/src/nuclear_data/data/extracted_text.txt"
    output_file = "/home/bas/src/nuclear_data/data/nubase2020_table_i.csv"
    
    print("Parsing NUBASE2020 Table I...")
    data = parse_nubase_table(text_file)
    
    if data:
        save_to_csv(data, output_file)
        print(f"\nExtracted Table I with {len(data)} nuclear entries")
    else:
        print("Failed to extract Table I data")