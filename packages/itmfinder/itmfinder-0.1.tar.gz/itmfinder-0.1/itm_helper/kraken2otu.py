# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:15:36 2023

@author: sipost1
"""
import os
import glob
import csv
import argparse
from collections import defaultdict
from typing import Dict, TextIO

def extract(file: str) -> Dict:
    """
    Requires a valid kraken2 report file.
    Returns a dictionary of taxa and read counts.
    """
    taxons = defaultdict(dict)

    # Standard kraken2 output has 6 fields.
    indexes = {6: [3, 5], 8: [5, 7]}
    file_path = os.path.abspath(file)

    with open(file_path, "r") as ori:
        lines = ori.readlines()

    assert len(lines) > 0, "Empty file!"

    taxon_index, name_index = indexes[len(lines[0].split("\t"))]
    print(f"Reading {file}")
    print(f"Used indexes: field {taxon_index + 1} for taxon rank, field {name_index + 1} for taxon name.")

    for line in lines:
        line_params = line.rstrip("\n").split("\t")
        read_count = line_params[1]
        taxon = line_params[taxon_index].strip()
        name = line_params[name_index].strip()
        taxons[taxon][name] = read_count

    return taxons

def read_in_files(directory: str, extension: str = ".k2report") -> Dict:
    """
    Reads k2report files from a directory and returns a 3-depth dictionary.
    """
    file_dictionary = defaultdict()
    report_files = glob.glob(f"{directory}/*{extension}")
    assert len(report_files) > 0, "No report file found! Please check filename extension and input directory!"

    for file in report_files:
        file = os.path.abspath(file)
        file_dictionary[os.path.basename(file).rstrip(extension)] = extract(file)

    return file_dictionary

def create_otu_table(level: str, file_sample_dict: Dict, outdir: str = "./") -> TextIO:
    """
    Creates an OTU table for a given taxonomic level.
    """
    rearranged_dict = defaultdict(dict)

    level = level.upper()
    sample_taxa = {sample: level_list[level] for sample, level_list in file_sample_dict.items()}

    for sample, taxon_list in sample_taxa.items():
        for taxon in taxon_list:
            rearranged_dict[taxon][sample] = taxon_list[taxon]

    headers = ["otu"] + list(sample_taxa.keys())
    outfile_name = f"otu_table_{level}.csv"
    with open(os.path.join(outdir, outfile_name), "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)  # Write headers

        for otu, inner_dict in rearranged_dict.items():
            row = [otu] + [inner_dict.get(header, 0) for header in headers[1:]]
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputfolder", "-i", type=str, required=True, help="Input folder where report files can be found.")
    parser.add_argument("--level", "-l", type=str, required=True, help="Taxonomic level to extract from kraken2 report.")
    parser.add_argument("--extension", "-e", default=".k2report", help="Extension of kraken2 report files. Default: .k2report")
    parser.add_argument("--outdir", "-o", type=str, default="./", help="Output directory to save OTU table files. Default: current directory")
    args = parser.parse_args()

    # Process files and generate OTU table
    file_dict = read_in_files(args.inputfolder, extension=args.extension)
    create_otu_table(args.level, file_dict, outdir=args.outdir)
    print("Done!")

# Only execute main if this script is run directly
if __name__ == "__main__":
    main()
