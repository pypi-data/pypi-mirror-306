import os
import argparse
from multiprocessing import Pool
from itmfinder.itm_helper.extract_kraken_reads import main as extract_reads_main

def print_colorful_message(message, color):
    """
    Print a colorful message to the console.

    Args:
        message (str): The message to be printed.
        color (str): The color code to be applied.
                     Choices include 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.
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
    print(colors[color] + message + end_color)

def compress_to_gz(file_path):
    """
    Compress the given file to a .gz file and remove the original.

    Args:
        file_path (str): Path to the file to be compressed.
    """
    import gzip
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f_in:
            with gzip.open(file_path + '.gz', 'wb') as f_out:
                f_out.writelines(f_in)
        os.remove(file_path)
        print(f"Compressed and removed original: {file_path}")
    else:
        print(f"File {file_path} not found. Compression skipped.")

def extract_microbiome_reads(sample_info, is_single_end=False, TID=None):
    """
    Extract microbiome reads for a given sample using the itmfinder extract_reads_main function.

    Args:
        sample_info (tuple): Contains information about the sample.
        is_single_end (bool): Indicates if the data is single-end (True) or paired-end (False).
        TID (list of int): Taxonomic IDs to extract reads for.
    """
    sample_id, fastq_r1, kraken_output, output_r1, path4_ku1, path5_mr = sample_info
    report_file = os.path.join(path4_ku1, f"{sample_id}.kraken.report.txt")
    task_complete_file = os.path.join(path5_mr, f"{sample_id}.task.complete")

    if os.path.exists(task_complete_file):
        print(f">>> Sample {sample_id} already processed. Skipping...")
        return

    if not TID:
        TID = [2, 10239, 4751, 2157]  # Default Taxonomic IDs

    if is_single_end:
        extract_reads_main(kraken_output=kraken_output, seq_file1=fastq_r1, output_file1=output_r1, taxids=TID, report_file=report_file)
    else:
        fastq_r2 = fastq_r1.replace("_R1", "_R2")
        output_r2 = output_r1.replace("_1", "_2")
        extract_reads_main(kraken_output=kraken_output, seq_file1=fastq_r1, seq_file2=fastq_r2, output_file1=output_r1, output_file2=output_r2, taxids=TID, report_file=report_file)

    # Mark the task as complete
    with open(task_complete_file, "w") as f:
        f.write("Task completed.")

    # Optionally compress the output files
    compress_to_gz(output_r1)
    if not is_single_end:
        compress_to_gz(output_r2)

    print(f">>>--- Sample {sample_id} processed successfully.")

def step4_extract_microbiome_reads(path3_hr, path4_ku1, path5_mr, batch_size=1, is_single_end=False, TID=None):
    """
    Process all samples to extract microbiome reads based on Kraken2 output.

    Args:
        path3_hr (str): Directory containing host-removed FASTQ files.
        path4_ku1 (str): Directory containing Kraken2 output files.
        path5_mr (str): Directory where extracted microbiome reads will be stored.
        batch_size (int): Number of samples to process in parallel.
        is_single_end (bool): Flag to indicate if the processing should be for single-end reads.
        TID (list of int): List of Taxonomic IDs to filter reads.
    """
    print_colorful_message("#########################################################", "blue")
    print_colorful_message(" ITMfinder: Identifying Intratumoral Microbiome pipeline ", "cyan")
    print_colorful_message("#########################################################", "blue")

    os.makedirs(path5_mr, exist_ok=True)

    fastq_files = [f for f in os.listdir(path3_hr) if f.endswith("_R1.fastq.gz")] if not is_single_end else [f for f in os.listdir(path3_hr) if f.endswith(".fastq.gz")]
    samples = [
        (f.replace("_R1.fastq.gz", "") if not is_single_end else f.replace(".fastq.gz", ""),
         os.path.join(path3_hr, f),
         os.path.join(path4_ku1, f"{f.replace('_R1.fastq.gz', '') if not is_single_end else f.replace('.fastq.gz', '')}.kraken.output.txt"),
         os.path.join(path5_mr, f"{f.replace('_R1.fastq.gz', '_mr_1.fastq')}" if not is_single_end else f.replace(".fastq.gz", "_mr.fastq")),
         path4_ku1, path5_mr) for f in fastq_files
    ]

    with Pool(processes=batch_size) as pool:
        pool.starmap(extract_microbiome_reads, [(sample, is_single_end, TID) for sample in samples])

    print(">>>=== Microbiome reads extraction completed.")

def main():
    parser = argparse.ArgumentParser(description="Step 4: Extract microbiome reads from Kraken2 output")
    parser.add_argument("--path3_hr", type=str, required=True, help="Path to host removed FASTQ files")
    parser.add_argument("--path4_ku1", type=str, required=True, help="Path to Kraken2 outputs")
    parser.add_argument("--path5_mr", type=str, required=True, help="Path to extracted microbiome reads")
    parser.add_argument("--batch_size", type=int, default=1, help="Number of samples to process simultaneously")
    parser.add_argument("--se", action='store_true', help="Use single-end processing. Default is paired-end.")
    parser.add_argument("--TID", nargs='*', type=int, help="Taxonomic IDs for filtering reads.")
    args = parser.parse_args()

    step4_extract_microbiome_reads(args.path3_hr, args.path4_ku1, args.path5_mr, args.batch_size, args.se, args.TID)

# Ensure the main function only runs if this file is executed directly
if __name__ == "__main__":
    main()


