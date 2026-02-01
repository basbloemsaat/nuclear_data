# used prompts

From data_sources/NUBASE2020.pdf extract Table I, from page 21 to 181 to a csv file. Implement `extract_table_from_pdf` in extract_nubase2020_table1.py. Store the resulting .txt in data_sources/tmp.

Treat each page as a separate table and concatenate them into a single .txt file.

Non-ASCII code points found: U+00B5 (µ), U+03B1..03C4 (Greek letters), U+2013 (en-dash), U+2019/201C/201D (typographic quotes), U+2212 (minus sign), U+2217 (asterisk operator) and ligatures U+FB01/U+FB02 (ﬁ, ﬂ). Make sure these are handled correctly. Also there are subscript and superscript characters. Convert them to their unicode characters.

I already included the headers for the csv file based on the table structure in the PDF in the constant `TABLE1_HEADER`
Use a library that extracts text line by line to extract the data.

Start by extracting the first page (page 21) and verify the output before proceeding to the full range.

Do not parse any structure, just text lines.

<!-- Ignore lines that start with an asterisk (\*) as they are footnotes. -->

---

From data_sources/tmp/nubase2020_table1.txt, clean and parse the data into a structured csv file. Put the resulting .csv in data_sources/tmp. Create a new script data_sources/src/nubase2020_table1_to_csv.py to do this.

The headers are: Nuclide, "Mass Excess (keV)","Excitation Energy (keV)","Half-life", Jπ, "Ens Reference", "Year of discovery", "Decay modes and intensities (%)"
