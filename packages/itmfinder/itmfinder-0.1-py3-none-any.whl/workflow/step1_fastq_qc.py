import os
import subprocess
import random
import argparse
from multiprocessing import Pool

def print_colorful_message(message, color):
    """
    Print a colorful message to the console.
    Args:
        message (str): The message to be printed.
        color (str): The color code to be applied.
                     Choices are 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.
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

def process_sample(file, path1_fastq, path2_fastp, num_threads, suffix1, se, length_required):
    """
    Processes a single FASTQ file using fastp.
    Args:
        file (str): File name of the FASTQ file.
        path1_fastq (str): Path where raw FASTQ files are located.
        path2_fastp (str): Path where processed files will be saved.
        num_threads (int): Number of threads for fastp.
        suffix1 (str): Suffix for the forward reads files.
        se (bool): Flag to indicate if the data is single-end.
        length_required (int): Minimum length of reads to keep after processing.
    """
    suffix2 = suffix1.replace("1", "2")
    if file.endswith(suffix1):
        forward_file = os.path.join(path1_fastq, file)
        sample_id = file[:-len(suffix1)]
        output_forward = os.path.join(path2_fastp, file)
        task_file = os.path.join(path2_fastp, f"{sample_id}.task.complete")

        if os.path.exists(output_forward) and os.path.exists(task_file):
            print(f"Skipped: {forward_file}")
            return

        print_colorful_message(f"Processing: {sample_id}", "green")

        try:
            if se:
                command = [
                    "fastp", "-i", forward_file, "-o", output_forward,
                    "--thread", str(num_threads), "--length_required", str(length_required),
                    "--n_base_limit", "6", "--compression", "6",
                    "--html", f"{path2_fastp}/{sample_id}_fastp.html"
                ]
            else:
                reverse_file = forward_file[:-len(suffix1)] + suffix2
                output_reverse = output_forward[:-len(suffix1)] + suffix2
                command = [
                    "fastp", "-i", forward_file, "-o", output_forward,
                    "-I", reverse_file, "-O", output_reverse,
                    "--thread", str(num_threads), "--length_required", str(length_required),
                    "--n_base_limit", "6", "--compression", "6",
                    "--html", f"{path2_fastp}/{sample_id}_fastp.html"
                ]
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            with open(task_file, 'w') as f:
                f.write("Processing complete for " + sample_id)
            print_colorful_message(f"Task complete for {sample_id}", "cyan")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {sample_id}: {e.stderr.decode()}")

def step1_fastq_qc(path1_fastq, path2_fastp, num_threads=8, suffix1="_1.fastq.gz", batch_size=5, se=False, length_required=50):
    """
    Preprocess FASTQ files using fastp in parallel.
    Args:
        path1_fastq (str): Path to raw FASTQ files.
        path2_fastp (str): Path to preprocessed FASTQ files.
        num_threads (int): Number of threads for fastp.
        suffix1 (str): Suffix for the forward reads files.
        batch_size (int): Number of samples to process simultaneously.
        se (bool): Flag to indicate if the sequencing data is single-end.
        length_required (int): Minimum length of reads to keep after processing.
    """
    print_colorful_message("#########################################################", "blue")
    print_colorful_message(" ITMfinder: Identifying Intratumoral Microbiome pipeline ", "cyan")
    print_colorful_message(" If you encounter any issues, please report them at ", "cyan")
    print_colorful_message(" https://github.com/LiaoWJLab/ITMtools/issues ", "cyan")
    print_colorful_message("#########################################################", "blue")
    print(" Author: Dongqiang Zeng, Qianqian Mao ")
    print(" Email: interlaken@smu.edu.cn ")
    print_colorful_message("#########################################################", "blue")

    print("### FASTQ files quality control using fastp ###")

    os.makedirs(path2_fastp, exist_ok=True)
    fastq_files = [f for f in os.listdir(path1_fastq) if f.endswith(suffix1)]
    random.shuffle(fastq_files)

    with Pool(processes=batch_size) as pool:
        pool.starmap(process_sample, [(file, path1_fastq, path2_fastp, num_threads, suffix1, se, length_required) for file in fastq_files])


# Keep the existing code as it is, but add a main function for import purposes
def main():
    parser = argparse.ArgumentParser(description="Preprocess FASTQ files using fastp")
    parser.add_argument("--path1_fastq", type=str, required=True, help="Path to raw FASTQ files")
    parser.add_argument("--path2_fastp", type=str, required=True, help="Path to preprocessed FASTQ files")
    parser.add_argument("--num_threads", type=int, default=8, help="Number of threads for fastp")
    parser.add_argument("--suffix1", type=str, default="_1.fastq.gz", help="Suffix of the forward reads file")
    parser.add_argument("--batch_size", type=int, default=5, help="Number of samples to process simultaneously")
    parser.add_argument("--se", action='store_true', help="Indicate if the sequencing data is single-end")
    parser.add_argument("--length_required", type=int, default=50, help="Minimum length of reads to keep after processing")
    args = parser.parse_args()

    step1_fastq_qc(args.path1_fastq, args.path2_fastp, args.num_threads, args.suffix1, args.batch_size, args.se, args.length_required)

# Ensure the main function only runs if this file is executed directly
if __name__ == "__main__":
    main()
