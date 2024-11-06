import os
import subprocess
import random
import argparse
from itmfinder.itm_helper.kreport2mpa import main as kreport2mpa_main

def print_colorful_message(message, color):
    """
    Print a colorful message to the console.

    Args:
        message (str): The message to be printed.
        color (str): The color code to be applied. 
                     'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
    }
    end_color = '\033[0m'
    if color not in colors:
        print("Invalid color. Please choose from 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.")
        return
    colored_message = f"{colors[color]}{message}{end_color}"
    print(colored_message)


def step3_kraken2(path3_hr, path4_ku1, db_ku, num_threads=8, se=False):
    """
    Perform taxonomic classification using Kraken2.

    Args:
        path3_hr (str): Path to host-removed FASTQ files.
        path4_ku1 (str): Path to Kraken2 outputs.
        db_ku (str): Path to Kraken2 database.
        num_threads (int): Number of threads for Kraken2 analysis. Default is 8.
        se (bool): Whether the data is single-end sequencing. Default is False.
    """
    print("   ")
    print_colorful_message("#########################################################", "blue")
    print_colorful_message(" ITMfinder: Identifing Intratumoral Microbiome pipeline ", "cyan")
    print_colorful_message(" If you encounter any issues, please report them at ", "cyan")
    print_colorful_message(" https://github.com/LiaoWJLab/ITMtools/issues ", "cyan")
    print_colorful_message("#########################################################", "blue")
    print(" Author: Dongqiang Zeng, Qianqian Mao ")
    print(" Email: interlaken@smu.edu.cn ")
    print_colorful_message("#########################################################", "blue")
    print("   ")

    # Create the output directory if it does not exist
    os.makedirs(path4_ku1, exist_ok=True)
    
    # List files in the host-removed FASTQ directory
    files = os.listdir(path3_hr)
    files = [file for file in files if file.endswith("_host_remove_R1.fastq.gz")]
    random.shuffle(files)  # Shuffle the files randomly
    total_files = len(files)
    current_file = 0
    
    for file in files:
        current_file += 1
        print(f"Processing file {current_file} of {total_files}: {file}")
        # Extract sample ID from the filename
        sample_id = file[:-len("_host_remove_R1.fastq.gz")]
        # Construct paths to input and output files
        input_fq1 = os.path.join(path3_hr, f"{sample_id}_host_remove_R1.fastq.gz")
        input_fq2 = os.path.join(path3_hr, f"{sample_id}_host_remove_R2.fastq.gz")
        output_file = os.path.join(path4_ku1, f"{sample_id}.kraken.output.txt")
        report = os.path.join(path4_ku1, f"{sample_id}.kraken.report.txt")
        report_std = os.path.join(path4_ku1, f"{sample_id}.kraken.report.std.txt")
        mpa_output = os.path.join(path4_ku1, f"{sample_id}.kraken.mpa.txt")
        task_complete = os.path.join(path4_ku1, f"{sample_id}.task.complete")
        # Check if the task is already completed
        if os.path.exists(task_complete) and os.path.getsize(report_std) > 0:
            print(f"{report_std} already exists, skipping...")
        else:
            # Run Kraken2 for taxonomic classification
            print(f">>>-- Running Kraken2 for taxonomic classification on sample {sample_id}...")
            if se:
                subprocess.run(["kraken2", "--db", db_ku, "--threads", str(num_threads), "--report-minimizer-data", "--report", report,
                                "--use-names", "--output", output_file, input_fq1])
            else:
                subprocess.run(["kraken2", "--db", db_ku, "--threads", str(num_threads), "--report-minimizer-data", "--report", report,
                                "--use-names", "--output", output_file, "--paired", input_fq1, input_fq2])
            # Process Kraken report to a more readable format
            print("      Processing Kraken report...")
            subprocess.run(f"cut -f1-3,6-8 {report} > {report_std}", shell=True)
            # Convert Kraken report to MPA format
            print("      Converting Kraken report to MPA format...")

            # Convert report to MPA format using directly imported function
            kreport2mpa_main(report_std, mpa_output)
            # subprocess.run(["kreport2mpa_main", "-r", report_std, "-o", mpa_output])
            # Create a task complete file
            open(task_complete, "w").close()
            print("   ")
    
    print("Kraken2 taxonomic classification completed.")

def main():
    parser = argparse.ArgumentParser(description="Step 3: Taxonomic classification using Kraken2")
    parser.add_argument("--path3_hr", type=str, help="Path to host removed FASTQ files")
    parser.add_argument("--path4_ku1", type=str, help="Path to Kraken2 outputs")
    parser.add_argument("--db_ku", type=str, help="Path to Kraken2 database")
    parser.add_argument("--num_threads", type=int, default=8, help="Number of threads")
    parser.add_argument("--se", action='store_true', help="Single-end sequencing data")
    args = parser.parse_args()

    step3_kraken2(args.path3_hr, args.path4_ku1, args.db_ku, args.num_threads, args.se)

# Ensure the main function only runs if this file is executed directly
if __name__ == "__main__":
    main()

