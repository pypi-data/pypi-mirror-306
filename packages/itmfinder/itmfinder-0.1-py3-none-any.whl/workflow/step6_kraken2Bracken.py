import os
import subprocess
import argparse
import random
from multiprocessing import Pool
from itmfinder.itm_helper.kreport2mpa import main as kreport2mpa_main
from itmfinder.itm_helper.alpha_diversity import main as alpha_diversity_main

def print_colorful_message(message, color):
    """
    Print a colorful message to the console.
    Args:
        message (str): The message to be printed.
        color (str): The color code to be applied.
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
    print(colors.get(color, '\033[97m') + message + end_color)

def process_sample(sample_id, paths, db_ku, num_threads, force):
    path6_rcr, path7_ku2, path8_bracken = paths
    kraken_output = os.path.join(path7_ku2, f"{sample_id}.kraken.output.txt")
    kraken_report = os.path.join(path7_ku2, f"{sample_id}.kraken.report.txt")
    task_complete_file = os.path.join(path7_ku2, f"{sample_id}.task.complete")

    # Check if processing is already completed
    if os.path.exists(task_complete_file) and os.path.exists(kraken_report) and not force:
        print_colorful_message(f"Sample {sample_id} processing already completed. Skipping...", "green")
        return

    print_colorful_message(f"Running Kraken2 and Bracken for sample: {sample_id}", "yellow")

    # Paths for paired-end fastq files
    fastq_files = [os.path.join(path6_rcr, f"{sample_id}_rcr_1.fastq.gz"), os.path.join(path6_rcr, f"{sample_id}_rcr_2.fastq.gz")]

    # Run Kraken2 for taxonomic classification
    subprocess.run(["kraken2", "--db", db_ku, "--threads", str(num_threads), "--paired", "--report-minimizer-data",
                    "--report", kraken_report, "--output", kraken_output] + fastq_files)

    # Convert Kraken report to MPA format
    kreport2mpa_main(report_path=kraken_report, output_path=os.path.join(path7_ku2, f"{sample_id}.kraken.mpa.txt"))

    # Define paths for Bracken outputs at various taxonomic levels
    bracken_outputs = {
        "G": os.path.join(path8_bracken, f"{sample_id}.g.bracken"),
        "S": os.path.join(path8_bracken, f"{sample_id}.s.bracken"),
        "F": os.path.join(path8_bracken, f"{sample_id}.f.bracken"),
        "O": os.path.join(path8_bracken, f"{sample_id}.o.bracken")
    }

    # Run Bracken for abundance estimation at different taxonomic levels
    for level, output in bracken_outputs.items():
        subprocess.run(["bracken", "-d", db_ku, "-i", kraken_report, "-o", output, "-r", "100", "-l", level, "-t", "2"])

    # Calculate alpha diversity for genus and species levels
    diversity_outputs = {
        "G": os.path.join(path8_bracken, f"{sample_id}.diversity.g.txt"),
        "S": os.path.join(path8_bracken, f"{sample_id}.diversity.s.txt")
    }

    # Execute alpha diversity calculations for each level
    for level, bracken_output in bracken_outputs.items():
        if level in diversity_outputs:
            diversity_output = diversity_outputs[level]
            with open(diversity_output, "a") as f:
                for metric in ["Sh", "BP", "Si", "ISi", "F"]:
                    # Call alpha_diversity_main with expected parameters
                    alpha_diversity_main(bracken_output, metric)

    # Mark task as completed
    with open(task_complete_file, "w") as f:
        f.write("Processing completed.")

def step6_kraken2Bracken(path6_rcr, path7_ku2, path8_bracken, db_ku, num_threads=8, force=False):
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
    print(" >>> Perform taxonomic classification using Kraken2...")

    os.makedirs(path7_ku2, exist_ok=True)
    os.makedirs(path8_bracken, exist_ok=True)

    # List all samples
    mr_files = [f for f in os.listdir(path6_rcr) if f.endswith("_rcr_1.fastq.gz")]
    random.shuffle(mr_files)  # Shuffle for random processing order
    paths = (path6_rcr, path7_ku2, path8_bracken)
    
    # Process samples in parallel
    with Pool() as pool:
        pool.starmap(process_sample, [(f.split('_')[0], paths, db_ku, num_threads, force) for f in mr_files])

    print_colorful_message("All samples have been processed.", "blue")

def main():
    parser = argparse.ArgumentParser(description="Step 6: Taxonomic classification using Kraken2 for report")
    parser.add_argument("--path6_rcr", type=str, required=True, help="Path to microbiome reads after decontamination")
    parser.add_argument("--path7_ku2", type=str, required=True, help="Path to store Kraken2 outputs")
    parser.add_argument("--path8_bracken", type=str, required=True, help="Path for Bracken outputs")
    parser.add_argument("--db_ku", type=str, required=True, help="Path to Kraken2 database")
    parser.add_argument("--num_threads", type=int, default=8, help="Number of threads")
    parser.add_argument("--force", action="store_true", help="Force execution of downstream Kraken2 process")
    args = parser.parse_args()

    step6_kraken2Bracken(args.path6_rcr, args.path7_ku2, args.path8_bracken, args.db_ku, args.num_threads, args.force)

# Ensure the main function only runs if this file is executed directly
if __name__ == "__main__":
    main()
