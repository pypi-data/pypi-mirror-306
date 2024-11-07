# ITMfinder: Identifying Intratumoral Microbiome

## Overview
**ITMfinder** is a powerful tool designed to identify and analyze intratumoral microbiomes using various sequencing data. It integrates tools such as Kraken2, Bracken, and several custom workflows to process and classify microbiome reads, offering users a straightforward, customizable pipeline for identifying and quantifying microbiome components within tumor tissue samples.

## Features
- **Multiple-step pipeline** for quality control, host removal, microbial classification, and abundance estimation.
- **Integration of popular bioinformatics tools** such as Kraken2 and Bracken for comprehensive microbiome analysis.
- **Decontamination and alpha diversity analysis** included in the workflow.

## Requirements
Before installing ITMfinder, make sure you have the following dependencies in your environment:
- Python 3.7 or higher
- Bioinformatics tools: Kraken2, Bracken, Fastp, Bowtie2, Biopython
- Conda package manager for dependency management

To install all required packages, you can use the provided `requirements.txt` file.

## Installation
1. Clone the repository from GitHub:
    ```sh
    git clone https://github.com/your-username/ITMfinder.git
    cd ITMfinder
    ```
2. Set up a virtual environment (optional but recommended):
    ```sh
    python -m venv itmfinder_env
    source itmfinder_env/bin/activate
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```
4. Install Kraken2:
    - Kraken2 and other bioinformatics tools like Bracken are installed separately, usually via Bioconda. Use:
      ```sh
      conda install -c bioconda kraken2 bracken fastp bowtie2
      ```

## Usage
Run ITMfinder by specifying the step of the workflow that you want to execute:

1. **Help Documentation**: To see the available steps and options, use:
   ```sh
   itmfinder -h
   ```

2. **Run a Step**: To run a specific step, use the `--step` argument followed by the step number (1-8). For example, to run step 1:
   ```sh
   itmfinder --step 1
   ```
   Additional arguments specific to each step can be added as needed.

3. **Workflow Steps**:
   - **Step 1**: FastQ Quality Control
   - **Step 2**: Remove Host Reads
   - **Step 3**: Kraken2 Classification
   - **Step 4**: Extract Microbiome Reads
   - **Step 5**: Decontaminate Microbiome Reads
   - **Step 6**: Bracken Taxonomic Classification
   - **Step 7**: Merge Results to OTU and MPA Formats
   - **Step 8**: Generate Data Summary

## Example
To run a complete analysis starting from FastQ files, follow these steps sequentially:
```sh
itmfinder --step 1 --input /path/to/input --output /path/to/output
itmfinder --step 2 --input /path/to/output_from_step1 --output /path/to/output_step2
...
itmfinder --step 8 --input /path/to/merged_results --output /path/to/summary
```

## File Structure
- `workflow/`: Contains individual Python scripts for each step in the workflow.
- `resources/`: Configuration files and contamination lists used in the workflow.
- `utils/`: Utility functions used throughout the pipeline.

## Requirements File (`requirements.txt`)
Ensure you have the following in `requirements.txt`:
```
biopython
pandas
bowtie2==2.5.1
bracken==2.8
fastp==0.23.3
kraken2==2.1.3
```

## License
This project is licensed under the MIT License.

## Support
If you encounter any issues, please report them at [GitHub Issues](https://github.com/your-username/ITMfinder/issues).

## Authors
- Dongqiang Zeng - [GitHub](https://github.com/dongqiangzeng)
- Qianqian Mao - [GitHub](https://github.com/qianqianmao)

## Citation
If you use ITMfinder in your research, please cite our repository or the associated publication.

