import os
import subprocess
import random
import argparse
from multiprocessing import Pool
from functools import partial

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

def process_sample(file, path3_hr, path3_hr2, db_bowtie2, suffix1, num_threads, se):
    """
    Process a single sample to remove host reads using Bowtie2.
    """
    try:
        # Extract sample ID from the filename
        sample_id = os.path.basename(file).replace(suffix1, "")  # Remove the suffix to get sample ID
        output = f"{sample_id}_host_remove"
        log_file = os.path.join(path3_hr2, f"{sample_id}_bowtie2.log") 

        # FOR SINGLE-END
        if se:
            output_file = f"{output}.fastq.gz"
            # Check if the output file already exists
            if os.path.exists(os.path.join(path3_hr2, output_file)):
                print(f"Skipped: {output_file} as it already exists.")
                return
            
            print(f" >>> Processing file: {file}")
            
            # Run Bowtie2 to remove host reads
            subprocess.run(["bowtie2", "-p", str(num_threads), "-x", db_bowtie2, "-U", os.path.join(path3_hr, file), 
                           "--un-gz", os.path.join(path3_hr2, output), "--no-unal"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Rename the output file
            os.rename(os.path.join(path3_hr2, f"{output}.fastq.gz"), os.path.join(path3_hr2, output_file))
            
        # FOR PAIRED-END
        else:
            output_file1 = f"{output}_R1.fastq.gz"
            output_file2 = f"{output}_R2.fastq.gz"

            # Check if the output files already exist
            if os.path.exists(os.path.join(path3_hr2, output_file1)) and os.path.exists(os.path.join(path3_hr2, output_file2)):
                print(f"Skipped: {output_file1} and {output_file2} as they already exist.")
                return
            
            # Determine the second-end filename
            sample_id_second_end = f"{output_file2}"

            print(f" >>> Processing files: {file} and {sample_id_second_end}")

            subprocess.run(["bowtie2", "-p", str(num_threads), "-x", db_bowtie2, "-1", os.path.join(path3_hr, file), 
                             "-2", os.path.join(path3_hr, sample_id_second_end), "--un-conc-gz", os.path.join(path3_hr2, output), "--no-unal"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Rename the output files
            os.rename(os.path.join(path3_hr2, f"{output}.1"), os.path.join(path3_hr2, output_file1))
            os.rename(os.path.join(path3_hr2, f"{output}.2"), os.path.join(path3_hr2, output_file2))
        
        # Create task.complete file
        open(os.path.join(path3_hr2, f"{sample_id}.task.complete"), 'a').close()

    except Exception as e:
        print(f"Error processing file {file}: {e}")

def step2_remove_host_reads(path3_hr, path3_hr2, db_bowtie2, suffix1="_host_remove_R1.fastq.gz", num_threads=8, batch_size=1, se=False):
    """
    Remove host reads from preprocessed FASTQ files using Bowtie2.

    Args:
        path3_hr (str): Path to preprocessed FASTQ files.
        path3_hr2 (str): Path to host removed FASTQ files.
        db_bowtie2 (str): Path to Bowtie2 database.
        suffix1 (str): Suffix of the forward reads file. Default is "_host_remove_R1.fastq.gz".
        num_threads (int): Number of threads to use for Bowtie2 alignment. Default is 8.
        batch_size (int): Batch size for concurrent processing. Default is 1.
        se (bool): Whether the data is single-end sequencing. Default is False.
    """

    print("   ")
    print_colorful_message("#########################################################", "blue")
    print_colorful_message(" ITMfinder: Identifing Intratumoral Microbiome pipeline ", "cyan")
    print_colorful_message(" If you encounter any issues, please report them at ", "cyan")
    print_colorful_message(" https://github.com/LiaoWJLab/ITMfinder/issues ", "cyan")
    print_colorful_message("#########################################################", "blue")
    print(" Author: Dongqiang Zeng, Qianqian Mao ")
    print(" Email: interlaken@smu.edu.cn ")
    print_colorful_message("#########################################################", "blue")
    print("   ")

    print(" >>> Step-2 Remove host gene reads...  ")

    # Create the output directory if it does not exist
    os.makedirs(path3_hr2, exist_ok=True)
    
    # Get the list of files in the input directory
    files = sorted([file for file in os.listdir(path3_hr) if file.endswith(suffix1)], reverse=True)
    random.shuffle(files)  # Shuffle the files randomly
    total_files = len(files)
    
    # Define partial function with fixed arguments
    partial_process_sample = partial(process_sample, path3_hr=path3_hr, path3_hr2=path3_hr2, db_bowtie2=db_bowtie2, suffix1=suffix1, num_threads=num_threads, se=se)
    
    # Iterate through the files in the input directory
    for index in range(0, total_files, batch_size):
        batch_files = files[index:index+batch_size]
        with Pool(processes=batch_size) as pool:
            pool.map(partial_process_sample, batch_files)

def main():
    parser = argparse.ArgumentParser(description="Step 2: Remove host reads using Bowtie2")
    parser.add_argument("--path3_hr", type=str, help="Path to host removed FASTQ files firstly")
    parser.add_argument("--path3_hr2", type=str, help="Path to host removed FASTQ files secondly")
    parser.add_argument("--db_bowtie2", type=str, help="Path to Bowtie2 database")
    parser.add_argument("--num_threads", type=int, default=8, help="Number of threads")
    parser.add_argument("--suffix1", type=str, default="_host_remove_R1.fastq.gz", help="Suffix of the forward reads file")
    parser.add_argument("--batch_size", type=int, default=1, help="Batch size for concurrent processing")
    parser.add_argument("--se", action='store_true', help="Single-end sequencing data")
    args = parser.parse_args()

    step2_remove_host_reads(args.path3_hr, args.path3_hr2, args.db_bowtie2, args.suffix1, args.num_threads, args.batch_size, args.se)

# Ensure the main function only runs if this file is executed directly
if __name__ == "__main__":
    main()

