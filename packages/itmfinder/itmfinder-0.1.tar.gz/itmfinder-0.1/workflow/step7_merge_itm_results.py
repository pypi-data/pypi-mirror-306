import os
import pandas as pd
import glob
from itmfinder.itm_helper.kraken2otu import main as kraken2otu_main
from itmfinder.itm_helper.combine_bracken_outputs import main as combine_bracken_main
from itmfinder.itm_helper.combine_mpa import main as combine_mpa_main


def print_colorful_message(message, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'white': '\033[97m',
    }
    end_color = '\033[0m'
    colored_message = f"{colors.get(color, '')}{message}{end_color}"
    print(colored_message)

def run_combine_bracken_outputs(path8_bracken, path_out):
    bracken_files = glob.glob(os.path.join(path8_bracken, "*.bracken"))
    level_mapping = {
        'g': 'genus',
        'f': 'family',
        'o': 'order',
        's': 'species'
    }

    for level, level_name in level_mapping.items():
        level_files = [file for file in bracken_files if file.endswith(f"{level}.bracken")]
        
        if not level_files:
            print(f"No {level}.bracken files found.")
            continue

        output_file = os.path.join(path_out, f"2-combined_bracken_results_{level_name}.txt")
        
        combine_bracken_main(
            files=level_files,
            output=output_file,
            taxonomy_level=level_name
        )
        print(f"Combined Bracken results saved to: {output_file}")

def step7_merge_itm_results(path7_ku2, path9_mpa, path8_bracken, mpa_suffix=".kraken.mpa.std.txt", report_suffix="kraken.report.txt", output_file="1-combine_mpa_std.txt"):
    os.makedirs(path9_mpa, exist_ok=True)

    print("   ")
    print_colorful_message("#########################################################", "blue")
    print_colorful_message(" ITMfinder: Identifying Intratumoral Microbiome pipeline ", "cyan")
    print_colorful_message(" If you encounter any issues, please report them at ", "cyan")
    print_colorful_message(" https://github.com/LiaoWJLab/ITMfinder/issues ", "cyan")
    print_colorful_message("#########################################################", "blue")
    print(" Author: Dongqiang Zeng, Qianqian Mao ")
    print(" Email: interlaken@smu.edu.cn ")
    print_colorful_message("#########################################################", "blue")
    print("   ")

    # Combine MPA files
    mpa_files = [file for file in os.listdir(path7_ku2) if file.lower().endswith(mpa_suffix) and os.path.getsize(os.path.join(path7_ku2, file)) > 0]
    if mpa_files:
        mpa_output_path = os.path.join(path9_mpa, output_file)
        combine_mpa_main(
            mpa_input_dir=path7_ku2,
            combined_output=mpa_output_path,
            level="all"
        )
        update_mpa_column_names(mpa_output_path, mpa_files, mpa_suffix)

    # Generate OTU tables
    levels = ["c", "o", "f", "g", "s"]
    empty_files = check_empty_files(path7_ku2)
    if empty_files:
        print_colorful_message(f"Warning: The following files are empty and will be deleted: {empty_files}", "yellow")
        for empty_file in empty_files:
            os.remove(empty_file)

    for level in levels:
        kraken2otu_main(
            kraken_input=path7_ku2,
            level=level,
            extension=report_suffix,
            output=os.path.join(path9_mpa, f"otu_table_{level}.csv")
        )

    # Combine Bracken outputs
    run_combine_bracken_outputs(path8_bracken, path9_mpa)

def update_mpa_column_names(file_path, mpa_files, mpa_suffix):
    df = pd.read_csv(file_path, sep='\t')
    sample_ids = [file.replace(mpa_suffix, "") for file in mpa_files]
    updated_column_names = ["TaxonID"] + sample_ids

    if len(updated_column_names) != len(df.columns):
        print("Column count mismatch in MPA output file.")
        return

    df.columns = updated_column_names
    df.to_csv(file_path, sep='\t', index=False)
    print("Updated column names in MPA file.")
    print(df.head())

def check_empty_files(path):
    empty_files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if file.endswith("kraken.report.txt") and os.path.getsize(file_path) == 0:
            print(f">>>== Empty file found: {file_path}. This file will be deleted.")
            empty_files.append(file_path)
    return empty_files

def main():
    parser = argparse.ArgumentParser(description="Step 7: Merge data to OTU and MPA formats")
    parser.add_argument("--path7_ku2", type=str, help="Path to Kraken2 outputs for report")
    parser.add_argument("--path9_mpa", type=str, help="Path to merged OTU and MPA data")
    parser.add_argument("--path8_bracken", type=str, help="Path to Bracken output files")
    parser.add_argument("--mpa_suffix", type=str, default=".kraken.mpa.std.txt", help="Suffix for MPA files. Default is '.kraken.mpa.std.txt'.")
    parser.add_argument("--report_suffix", type=str, default="kraken.report.txt", help="Suffix for report files. Default is 'kraken.report.txt'.")
    parser.add_argument("--output_file", type=str, default="1-combine_mpa_std.txt", help="Name of the output file. Default is '1-combine_mpa_std.txt'.")
    args = parser.parse_args()

    step7_merge_itm_results(args.path7_ku2, args.path9_mpa, args.path8_bracken, args.mpa_suffix, args.report_suffix, args.output_file)

# Ensure the main function only runs if this file is executed directly
if __name__ == "__main__":
    main()

