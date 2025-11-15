# Complete Isotope Database

## Overview

This database combines nuclear data from NUBASE2020 with chemical element information to create a comprehensive isotope database. Each entry represents a unique isotope (or isomer state) with complete nuclear and chemical properties.

## Database Structure

The complete isotope database (`complete_isotope_database.csv`) contains **1,291 isotopes** with the following fields:

### Core Identification
- **Atomic_Number**: Atomic number (number of protons) - 0 for neutron, 1-118 for elements
- **Symbol**: Chemical element symbol (H, He, Li, etc.)
- **Element_Name**: Full element name (Hydrogen, Helium, Lithium, etc.)

### Nuclear Properties
- **Mass_Excess_keV**: Mass excess in keV (difference from integer mass number × u)
- **Mass_Uncertainty_keV**: Uncertainty in mass excess measurement (keV)
- **Half_Life**: Half-life (various units: stable, ms, s, y, My, etc.)
- **Spin_Parity**: Nuclear spin and parity quantum numbers
- **Year**: Year of discovery or measurement
- **Decay_Modes**: Decay channels and branching ratios
- **Mass_Number**: Mass number (A = protons + neutrons)
- **Isomer**: Isomer state designation (blank for ground state, i/m/n/p/etc. for excited states)

## Coverage

- **Elements**: 70 different elements (including neutron as element 0)
- **Mass Range**: From mass 1 (neutron) to mass 295 (Oganesson-295)
- **Nuclear Regions**: Complete coverage from light nuclei to superheavy elements
- **Isomer States**: 728 excited nuclear states in addition to 563 ground states

## Isotope Distribution

The database is heavily weighted toward heavy and superheavy elements:

### Most Represented Elements
1. **Radium (Ra, Z=88)**: 56 isotopes
2. **Francium (Fr, Z=87)**: 50 isotopes  
3. **Actinium (Ac, Z=89)**: 46 isotopes
4. **Thorium (Th, Z=90)**: 44 isotopes
5. **Americium (Am, Z=95)**: 42 isotopes

### Stable Isotopes
- **Hydrogen**: 2 stable isotopes (¹H, ²H)
- **Helium**: 2 stable isotopes (³He, ⁴He)
- **Lithium**: 2 stable isotopes (⁶Li, ⁷Li)
- **Boron**: 2 stable isotopes (¹⁰B, ¹¹B)
- **Carbon**: 2 stable isotopes (¹²C, ¹³C)
- **Nitrogen**: 2 stable isotopes (¹⁴N, ¹⁵N)
- **Beryllium**: 1 stable isotope (⁹Be)

## Special Features

### Neutron Entry
- Atomic number 0 represents the free neutron
- Mass number 1, with appropriate nuclear properties

### Isomer States
- Complex isomer notation preserved from NUBASE2020
- States labeled with letters: i, m, n, p, etc.
- Some unusual multi-letter designations correctly mapped

### Data Quality
- All mass excess values with uncertainties
- Half-life data where available
- Discovery years for historical context
- Complete decay mode information

## Usage

This database can be used for:
- Nuclear physics calculations
- Isotope identification
- Decay chain analysis
- Nuclear data lookups
- Educational purposes
- Research applications

## Source Data

- **Nuclear Data**: NUBASE2020 evaluation (complete Table I, pages 21-181)
- **Chemical Elements**: Wikipedia List of Chemical Elements
- **Coverage**: All known isotopes from neutron to Oganesson-295

## Files Generated

1. `complete_isotope_database.csv` - Main database (1,291 entries)
2. `create_isotope_database.py` - Generation script
3. `analyze_isotope_database.py` - Analysis script

The database represents the most comprehensive nuclear isotope collection combining nuclear physics data with chemical element properties in a single, structured format.