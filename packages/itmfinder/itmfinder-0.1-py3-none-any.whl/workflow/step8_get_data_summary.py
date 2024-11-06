import os
import pandas as pd
import argparse

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


def get_file_size(filepath):
    """Get file size in MB"""
    if not os.path.exists(filepath):  # 检查文件是否存在
        raise FileNotFoundError(f"File '{filepath}' does not exist.")
    
    if not os.path.isfile(filepath):  # 检查路径是否指向一个文件
        raise ValueError(f"'{filepath}' is not a valid file path.")
    
    # 获取文件大小并返回
    return round(os.path.getsize(filepath) / (1024 * 1024), 2)
    

def get_files_and_sizes(directory, suffix):
    """Get filenames and sizes for files with specified suffix in directory"""
    files_and_sizes = []
    for file in os.listdir(directory):
        if file.endswith(suffix):
            filepath = os.path.join(directory, file)
            file_size = get_file_size(filepath)
            files_and_sizes.append((file, file_size))
    return files_and_sizes

def process_data_for_sample(sample_id, path2_fastp, path3_hr, path7_ku2, path6_rcr):
    """Process files for a single sample"""
    sample_data = []
    
    # Process files for path2_fastp
    fastp_files = get_files_and_sizes(os.path.join(path2_fastp), f"{sample_id}_1.fastq.gz")  # Only process single-end files
    # print("Fastp files:", fastp_files)
    
    # Process files for path3_hr
    hr_files = get_files_and_sizes(os.path.join(path3_hr), f"{sample_id}_host_remove_R1.fastq.gz")  # Only process single-end files
    # print("Host-removed files:", hr_files)
    
    # Process files for path6_rcr
    mr_files = get_files_and_sizes(os.path.join(path6_rcr), f"{sample_id}_rcr_1.fastq")  # Only process single-end files
    # print("Microbiome files:", mr_files)

    # Process files for path7_ku2
    ku2_file = get_files_and_sizes(os.path.join(path7_ku2), f"{sample_id}.kraken.output.txt")
    # print("Kraken files:", ku2_file)

    # Ensure all lists have the same length
    min_length = min(len(fastp_files), len(hr_files), len(mr_files))
    
    # Combine fastp_files, hr_files, and mr_files using zip and iterate over them
    for i in range(min_length):
        sample_data.append((sample_id, fastp_files[i][0], fastp_files[i][1], hr_files[i][0], hr_files[i][1], ku2_file[0][0], ku2_file[0][1], mr_files[i][0], mr_files[i][1]))
    
    return sample_data

def get_data_summary(path2_fastp, path3_hr, path7_ku2, path6_rcr, out_dir):
    """Process files for each sample and organize into a dataframe"""

    print("   ")
    print_colorful_message("#########################################################", "blue")
    print_colorful_message(" ITMfinder: Identifing Intratumoral Microbiome pipline", "cyan")
    print_colorful_message(" If you encounter any issues, please report them at ", "cyan")
    print_colorful_message(" https://github.com/LiaoWJLab/ITMtools/issues ", "cyan")
    print_colorful_message("#########################################################", "blue")
    print(" Author: Dongqiang Zeng, Qianqian Mao ")
    print(" Email: interlaken@smu.edu.cn ")
    print("   ")

    all_sample_data = []
    for file in os.listdir(path2_fastp):
        # Extract sample_id by removing suffixes like '_1.fastq.gz'
        sample_id = file.replace("_1.fastq.gz", "").replace("_2.fastq.gz", "")
        
        # Process data for the current sample
        sample_data = process_data_for_sample(sample_id, path2_fastp, path3_hr, path7_ku2, path6_rcr)
        all_sample_data.extend(sample_data)

    # Create a dataframe
    df = pd.DataFrame(all_sample_data, columns=["Sample", "Fastp_File", "Fastp_Size_MB",
                                                 "Host_Removed_File", "HR_Size_MB",
                                                 "Kraken_Output_File", "KU2_Size_MB",
                                                 "Microbiome_files", "Microbiome_Size_MB"])
    
    # Remove duplicate rows based on the first column 'Sample'
    df.drop_duplicates(subset=['Sample'], inplace=True)
    
    # Sort dataframe by 'Microbiome_Size_MB' column in descending order
    df.sort_values(by='Microbiome_Size_MB', ascending=False, inplace=True)
    
    print("Dataframe:")
    print(df)
    
    # Save the dataframe to the output directory
    output_file = os.path.join(out_dir, "0-sample_file_sizes.csv")
    df.to_csv(output_file, index=False)
    print(f"Sample file sizes saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Process files for each sample and organize into a dataframe")
    parser.add_argument("--path2_fastp", type=str, help="Path to preprocessed FASTQ files")
    parser.add_argument("--path3_hr", type=str, help="Path to host-removed FASTQ files")
    parser.add_argument("--path7_ku2", type=str, help="Path to Kraken output files")
    parser.add_argument("--path6_rcr", type=str, help="Path to microbiome reads")
    parser.add_argument("--out_dir", type=str, help="Output directory")
    args = parser.parse_args()

    get_data_summary(args.path2_fastp, args.path3_hr, args.path7_ku2, args.path6_rcr, args.out_dir)

# Ensure the main function only runs if this file is executed directly
if __name__ == "__main__":
    main()

