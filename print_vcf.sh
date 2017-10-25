#!/bin/bash

# prepare individal vcf for sampele of interest

vcf1=$1
vcf2=$2
sample1=$3
sample2=$4
#vcf_dir=$4

if [ ! -d vcf ]; then mkdir vcf ; fi

#bcftools view -e 'GT~"0/0"' -s $sample1 $vcf1 > vcf/$sample1.1.vcf <-- Inacurate filtering
#bcftools view -e 'GT~"0/0"' -s $sample2 $vcf2 > vcf/$sample2.2.vcf <-- Inacurate filtering

bcftools view -s $sample1 $vcf1 | bcftools annotate -x INFO,^FORMAT/GT | bcftools view -e 'GT="0/0"|GT="./."' > vcf/$sample1.1.vcf
bcftools view -s $sample2 $vcf2 | bcftools annotate -x INFO,^FORMAT/GT | bcftools view -e 'GT="0/0"|GT="./."' > vcf/$sample2.2.vcf
