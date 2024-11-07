# ./workflow/__init__.py

from .step1_fastq_qc import step1_fastq_qc as step1_fastq_qc_main
from .step2_remove_host_reads import step2_remove_host_reads as step2_remove_host_reads_main

from .step2_remove_host_reads2 import step2_remove_host_reads2 as step2_remove_host_reads2_main

from .step3_kraken2 import step3_kraken2 as step3_kraken2_main

from .step4_extract_microbiome_reads import step4_extract_microbiome_reads as step4_extract_microbiome_reads_main

from .step5_decontamination import step5_decontamination as step5_decontamination_main

from .step6_kraken2Bracken import step6_kraken2Bracken as step6_kraken2Bracken_main

from .step7_merge_itm_results import step7_merge_itm_results as step7_merge_itm_results_main

from .step8_get_data_summary import step8_get_data_summary as step8_get_data_summary_main
