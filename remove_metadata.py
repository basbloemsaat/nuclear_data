#!/usr/bin/env python3
"""
Remove metadata key from all isotope JSON files to minimize file sizes.
"""

import json
import os
from pathlib import Path

def remove_metadata_from_file(filepath):
    """Remove metadata key from a single JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove metadata key if it exists
        if 'metadata' in data:
            del data['metadata']
        
        # Write back the cleaned data
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Failed to process {filepath}: {e}")
        return False

def main():
    print("Removing metadata from all isotope JSON files...")
    
    isotopes_dir = Path('data/isotopes')
    
    if not isotopes_dir.exists():
        print(f"Directory {isotopes_dir} does not exist!")
        return
    
    # Get all isotope JSON files (excluding sources.json and index.json)
    isotope_files = [f for f in isotopes_dir.glob('*.json') 
                     if f.name not in ['sources.json', 'index.json']]
    
    print(f"Found {len(isotope_files)} isotope files to process")
    
    # Track statistics
    processed = 0
    failed = 0
    total_size_before = 0
    total_size_after = 0
    
    # Calculate size before processing
    for filepath in isotope_files:
        total_size_before += os.path.getsize(filepath)
    
    # Process each file
    for i, filepath in enumerate(isotope_files):
        if remove_metadata_from_file(filepath):
            processed += 1
        else:
            failed += 1
        
        # Progress indicator
        if (i + 1) % 200 == 0:
            print(f"  Processed {i + 1} files...")
    
    # Calculate size after processing
    for filepath in isotope_files:
        total_size_after += os.path.getsize(filepath)
    
    print(f"\nProcessing complete!")
    print(f"Successfully processed: {processed} files")
    print(f"Failed: {failed} files")
    
    # Show size savings
    size_saved = total_size_before - total_size_after
    percent_saved = (size_saved / total_size_before * 100) if total_size_before > 0 else 0
    
    print(f"\nStorage optimization:")
    print(f"Size before: {total_size_before / 1024:.1f} KB")
    print(f"Size after: {total_size_after / 1024:.1f} KB")
    print(f"Space saved: {size_saved / 1024:.1f} KB ({percent_saved:.1f}%)")
    print(f"Average file size: {total_size_after / len(isotope_files):.0f} bytes")
    
    # Show sample of processed file
    if isotope_files:
        sample_file = isotope_files[0]
        print(f"\nSample content from {sample_file.name}:")
        with open(sample_file, 'r') as f:
            sample_content = json.load(f)
        
        print("File structure:")
        for key in sample_content:
            if isinstance(sample_content[key], dict):
                print(f"  - {key}: {list(sample_content[key].keys())}")
            else:
                print(f"  - {key}: {type(sample_content[key]).__name__}")

if __name__ == "__main__":
    main()