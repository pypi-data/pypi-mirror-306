import os
import gzip
from multiprocessing import Pool
from itmfinder.itm_helper.extract_kraken_reads import main as extract_reads_main
from itmfinder.utils.data_loader import load_contamination_list

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

def compress_to_gz(file_path):
    """
    Compress the specified file to a gzipped version and remove the original.
    Args:
        file_path (str): Path to the file that needs to be compressed.
    """
    if file_path and os.path.exists(file_path):
        with open(file_path, 'rb') as f_in:
            with gzip.open(file_path + '.gz', 'wb') as f_out:
                f_out.writelines(f_in)
        os.remove(file_path)
    else:
        print(f"File {file_path} not found or invalid. Compression skipped.")

def rmc_extract_microbiome_reads(sample_info, is_single_end=False):
    """
    Perform extraction and decontamination on microbiome reads using contamination IDs.
    Args:
        sample_info (tuple): Contains information about the sample.
        is_single_end (bool): Flag to indicate if the sample is single-end.
    """
    sample_id, fastq_r1, kraken_output, path4_ku1, path6_rcr = sample_info
    output_r1 = os.path.join(path6_rcr, f"{sample_id}_clean.fastq.gz")
    report_file = os.path.join(path4_ku1, f"{sample_id}.kraken.report.txt")
    task_complete_file = os.path.join(path6_rcr, f"{sample_id}.task.complete")

    if os.path.exists(task_complete_file):
        print(f">>> Sample {sample_id} already processed. Skipping...")
        return

    contamination_ids = load_contamination_list()

    print_colorful_message(f"Running decontamination process for sample {sample_id}...", "cyan")

    # Call the function from itmfinder package
    extract_reads_main(kraken_file=kraken_output, seq_file1=fastq_r1, output_file=output_r1,
                       taxid=contamination_ids, exclude=True, include_children=True, report_file=report_file)

    # Check if processing is completed by checking if output files are created
    if os.path.exists(output_r1):
        with open(task_complete_file, 'w') as f:
            f.write("Task completed.")
        print(f">>>--- Sample {sample_id} processed successfully.")
        compress_to_gz(output_r1)
    else:
        print(f"Error occurred while processing sample {sample_id}.")

def step5_decontamination(path5_mr, path4_ku1, path6_rcr, batch_size=1, is_single_end=False):
    """
    Coordinate the decontamination process for multiple samples.
    """
    print_colorful_message("#########################################################", "blue")
    print_colorful_message(" ITMfinder: Identifying Intratumoral Microbiome pipeline ", "cyan")
    print_colorful_message("#########################################################", "blue")
    print(" Author: Dongqiang Zeng, Qianqian Mao ")
    print(" Email: interlaken@smu.edu.cn ")
    print_colorful_message("#########################################################", "blue")
    print("   ")

    os.makedirs(path6_rcr, exist_ok=True)
    fastq_files = [f for f in os.listdir(path5_mr) if f.endswith("_mr.fastq.gz")]

    samples = [(f.replace("_mr.fastq.gz", ""), os.path.join(path5_mr, f), os.path.join(path4_ku1, f"{f.replace('_mr.fastq.gz', '')}.kraken.output.txt"),
                path4_ku1, path6_rcr) for f in fastq_files]

    with Pool() as pool:
        pool.map(rmc_extract_microbiome_reads, samples)

    print(">>>=== Microbiome reads extraction completed.")

def main():
    parser = argparse.ArgumentParser(description="Decontaminate microbiome reads from Kraken2 output")
    parser.add_argument("--path5_mr", type=str, help="Path to extracted microbiome reads")
    parser.add_argument("--path4_ku1", type=str, help="Path to Kraken2 outputs")
    parser.add_argument("--path6_rcr", type=str, help="Path to decontaminated microbiome reads")
    parser.add_argument("--batch_size", type=int, default=1, help="Number of samples to process simultaneously")
    parser.add_argument("--se", action="store_true", help="Use single-end processing. Default is paired-end.")
    args = parser.parse_args()

    step5_decontamination(args.path5_mr, args.path4_ku1, args.path6_rcr, args.batch_size, args.se)
# Ensure the main function only runs if this file is executed directly
if __name__ == "__main__":
    main()

