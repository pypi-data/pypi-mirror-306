#!/usr/bin/env python
####################################################################
#kreport2mpa.py converts a Kraken-style report into mpa [MetaPhlAn) format
#Copyright (C) 2017-2020 Jennifer Lu, jennifer.lu717@gmail.com

#This file is part of KrakenTools.
#KrakenTools is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the license, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of 
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, see <http://www.gnu.org/licenses/>.

####################################################################
#Jennifer Lu, jlu26@jhmi.edu
#11/06/2017
#Updated: 07/12/2020
#
#This program reads in a Kraken report file and generates
#an mpa-format (MetaPhlAn) style report. Each line represents
#a possible taxon classification. The first column is lists the 
#domain, kingdom, phyla, etc, leading up to each taxon.
#The levels are separated by the | delimiter, with the type of 
#level specified before each name with a single letter and underscore
#(d_ for domain, k_ for kingdom, etc). 
#The second column is the number of reads classified within 
#that taxon's subtree.
#
#Input file:
#   - Kraken report file generates from the kraken raw output file
#Input Parameters to Specify [OPTIONAL]:
#   - header_line = prints a header line in mpa-report 
#       [Default: no header]
#   - intermediate-ranks = includes non-traditional taxon levels
#       (traditional levels: domain, kingdom, phylum, class, order, 
#       family, genus, species)
#       [Default: no intermediate ranks]
#Output file format (tab-delimited)
#   - Taxonomy tree levels |-delimited, with level type [d,k,p,c,o,f,g,s,x]
#   - Number of reads within subtree of the specified level
#
#Methods
#   - main
#   - process_kraken_report
#
#!/usr/bin/env python
import os
import argparse

def process_kraken_report(curr_str, remove_spaces):
    split_str = curr_str.strip().split('\t')
    if len(split_str) < 4:
        return []
    try:
        int(split_str[1])
    except ValueError:
        return []
    percents = float(split_str[0])
    all_reads = int(split_str[1])
    try:
        taxid = int(split_str[-3]) 
        level_type = split_str[-2]
        map_kuniq = {'species':'S', 'genus':'G','family':'F', 'order':'O', 'class':'C', 'phylum':'P', 'superkingdom':'D', 'kingdom':'K'}
        level_type = map_kuniq.get(level_type, '-')
    except ValueError:
        taxid = int(split_str[-2])
        level_type = split_str[-3]

    spaces = 0
    name = split_str[-1]
    while name.startswith(' '):
        name = name[1:]
        spaces += 1
    if remove_spaces:
        name = name.replace(' ', '_')
    level_num = spaces // 2
    return [name, level_num, level_type, all_reads, percents]

def kreport2mpai(r_file_path, o_file_path, add_header=False, use_reads=True, x_include=False, remove_spaces=True):
    curr_path = [] 
    prev_lvl_num = -1
    with open(r_file_path, 'r') as r_file, open(o_file_path, 'w') as o_file:
        if add_header:
            o_file.write("#Classification\t" + os.path.basename(r_file_path) + "\n")
        
        main_lvls = ['R', 'K', 'D', 'P', 'C', 'O', 'F', 'G', 'S']
        for line in r_file:
            report_vals = process_kraken_report(line, remove_spaces)
            if len(report_vals) < 5: 
                continue
            [name, level_num, level_type, all_reads, percents] = report_vals
            if level_type == 'U':
                continue
            level_type = "x" if level_type not in main_lvls else level_type.lower() if level_type == "D" else level_type
            level_str = level_type + "__" + name

            if prev_lvl_num == -1:
                prev_lvl_num = level_num
                curr_path.append(level_str)
            else:
                while level_num != (prev_lvl_num + 1):
                    prev_lvl_num -= 1
                    curr_path.pop()

                if (level_type == "x" and x_include) or level_type != "x":
                    for string in curr_path:
                        if (string[0] == "x" and x_include) or string[0] != "x":
                            if string[0] != "r": 
                                o_file.write(string + "|")
                    o_file.write(level_str + "\t" + str(all_reads if use_reads else percents) + "\n")
                curr_path.append(level_str)
                prev_lvl_num = level_num

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--report-file', '--report', required=True, dest='r_file', help='Input kraken report file for converting')
    parser.add_argument('-o', '--output', required=True, dest='o_file', help='Output mpa-report file name')
    parser.add_argument('--display-header', action='store_true', dest='add_header', default=False, help='Include header in mpa-report file')
    parser.add_argument('--read_count', action='store_true', dest='use_reads', default=True, help='Use read count for output [default]')
    parser.add_argument('--percentages', action='store_false', dest='use_reads', default=True, help='Use percentages for output')
    parser.add_argument('--intermediate-ranks', action='store_true', dest='x_include', default=False, help='Include non-traditional taxonomic ranks')
    parser.add_argument('--no-intermediate-ranks', action='store_false', dest='x_include', default=False, help='Exclude non-traditional taxonomic ranks [default]')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--remove-spaces', action='store_true', dest='remove_spaces', default=True, help='Replace spaces with underscores in taxon names [default]')
    group.add_argument('--keep-spaces', action='store_false', dest='remove_spaces', default=False, help='Keep spaces in taxon names')
    args = parser.parse_args()

    kreport2mpai(args.r_file, args.o_file, add_header=args.add_header, use_reads=args.use_reads, x_include=args.x_include, remove_spaces=args.remove_spaces)

if __name__ == "__main__":
    main()
