Compare Variants
Primarily designed for NGS validation and QC by comparing the number of variants called against a reference callset.

Prerequisites
1. <sample>.vcf.gz & .tbi  
 experimental results
2. <reference>.vcf.gz & .tbi  
 reference data (e.g. 1000 genomes project, platinum genomes, WGS results, etc.)
 preprocession needed, depending on vcf format: 0/1 vs 0|1, 1 vs chr1, etc.
3. config_batch.ini
4. sample.list
  one pair of samples per line. tab delimited
5. dictionary.txt
  CHROM:POS:REF:ALT, Gene.knowngene. tab delimited
  
Running
clone scripts in src/ to working directory
$ python run_compare_batch.py

Outputs
1. vcf/
  vcf file for each sample and reference
2. outputsnp/ and outputindel/
  intermediate files for CPRA comparison
3. summary/
  a. batchsummarysnp.txt and batchsummaryindel.txt
    counts of variants, TP, FP, FN, precision, and recall for each sample
  b. genecounttable.snp.txt and genecounttable.indel.txt
    counts of variants broken down in gene for all samples

