#!/usr/bin/env python3
"""
Analyze the complete isotope database and provide summary information.
"""

import pandas as pd

def main():
    print("Complete Isotope Database Analysis")
    print("="*50)
    
    # Read the database
    df = pd.read_csv('data/complete_isotope_database.csv')
    
    print(f"Total isotopes in database: {len(df)}")
    print(f"Elements represented: {df['Atomic_Number'].nunique()}")
    print(f"Mass number range: {df['Mass_Number'].min()} to {df['Mass_Number'].max()}")
    
    print(f"\nColumn information:")
    print(f"- Atomic_Number: {df['Atomic_Number'].describe()}")
    print(f"- Mass_Number: {df['Mass_Number'].describe()}")
    
    print(f"\nIsotope distribution by element (top 15):")
    element_counts = df.groupby(['Atomic_Number', 'Symbol', 'Element_Name']).size().sort_values(ascending=False)
    for (z, symbol, name), count in element_counts.head(15).items():
        z_str = str(int(z)) if pd.notna(z) else "0"
        print(f"  {z_str:3s} {symbol:2s} {name:15s}: {count:3d} isotopes")
    
    print(f"\nElements with the most stable isotopes:")
    stable_isotopes = df[df['Half_Life'] == 'STABLE']
    stable_counts = stable_isotopes.groupby(['Atomic_Number', 'Symbol', 'Element_Name']).size().sort_values(ascending=False)
    for (z, symbol, name), count in stable_counts.head(10).items():
        z_str = str(int(z)) if pd.notna(z) else "0"
        print(f"  {z_str:3s} {symbol:2s} {name:15s}: {count:3d} stable isotopes")
    
    print(f"\nIsomer states:")
    isomer_counts = df['Isomer'].value_counts()
    print(f"- Ground states (no isomer): {isomer_counts.get('', 0) + pd.isna(df['Isomer']).sum()}")
    print(f"- Isomer states: {len(df) - (isomer_counts.get('', 0) + pd.isna(df['Isomer']).sum())}")
    
    print(f"\nSample entries from different mass regions:")
    
    print(f"\nLight nuclei (A < 20):")
    light = df[df['Mass_Number'] < 20].head(5)
    print(light[['Atomic_Number', 'Symbol', 'Element_Name', 'Mass_Number', 'Half_Life', 'Isomer']].to_string(index=False))
    
    print(f"\nMedium nuclei (20 <= A < 100):")
    medium = df[(df['Mass_Number'] >= 20) & (df['Mass_Number'] < 100)].sample(5)
    print(medium[['Atomic_Number', 'Symbol', 'Element_Name', 'Mass_Number', 'Half_Life', 'Isomer']].to_string(index=False))
    
    print(f"\nHeavy nuclei (A >= 200):")
    heavy = df[df['Mass_Number'] >= 200].tail(5)
    print(heavy[['Atomic_Number', 'Symbol', 'Element_Name', 'Mass_Number', 'Half_Life', 'Isomer']].to_string(index=False))

if __name__ == "__main__":
    main()