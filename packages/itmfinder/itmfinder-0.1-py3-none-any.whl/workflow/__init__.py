# This file makes it possible to import main functions directly from the package level
# ./workflow/__init__.py
from .step1_fastq_qc import main as step1_fastq_qc
from .step2_remove_host_reads import main as step2_remove_host_reads
from .step3_kraken2 import main as step3_kraken2
from .step4_extract_microbiome_reads import main as step4_extract_microbiome_reads
from .step5_decontamination import main as step5_decontamination
from .step6_kraken2Bracken import main as step6_kraken2Bracken
from .step7_merge_itm_results import main as step7_merge_itm_results
from .step8_get_data_summary import main as step8_get_data_summary

# Optionally, define a list of all main functions to simplify access further, e.g.,
all_steps = [step1_fastq_qc, step2_remove_host_reads, step3_kraken2, step4_extract_microbiome_reads,
             step5_decontamination, step6_kraken2Bracken, step7_merge_itm_results, step8_get_data_summary]
