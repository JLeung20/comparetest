#!/bin/bash

sample1=$1
sample2=$2
vcf_dir=$3
out_dir=$4
mode=$5
type=$6

if [ ! -d $out_dir ]; then mkdir $out_dir ; fi

# remove vcf header and create CPRA
#bcftools annotate -x INFO,^FORMAT/GT $vcf_dir/$sample1.1.vcf | bcftools view -H | awk -v var="$sample1" '{print $1":"$2":"$4":"$5":"$10"\t"var}' > $out_dir/$sample1.1.cpra
#bcftools annotate -x INFO,^FORMAT/GT $vcf_dir/$sample2.2.vcf | bcftools view -H | awk -v var="$sample2" '{print $1":"$2":"$4":"$5":"$10"\t"var}' > $out_dir/$sample2.2.cpra

vcftools --vcf $vcf_dir/$sample1.1.vcf --recode --$mode --out $vcf_dir/$sample1.1.$type
vcftools --vcf $vcf_dir/$sample2.2.vcf --recode --$mode --out $vcf_dir/$sample2.2.$type

bcftools view -H $vcf_dir/$sample1.1.$type.recode.vcf| awk -v var="$sample1" '{print $1":"$2":"$4":"$5":"$10"\t"var}' > $out_dir/$sample1.1.cpra
bcftools view -H $vcf_dir/$sample2.2.$type.recode.vcf| awk -v var="$sample2" '{print $1":"$2":"$4":"$5":"$10"\t"var}' > $out_dir/$sample2.2.cpra

# compare cpra and generate .diff
printf "Summary:\n\nFile ONE:\n" > $out_dir/$sample1.cpra.$type.diff
awk -F ':' '{print $5}' $out_dir/$sample1.1.cpra | sort | uniq -c >> $out_dir/$sample1.cpra.$type.diff
totalone=$(awk -F ':' '{print $5}' $out_dir/$sample1.1.cpra| sort | uniq -c | awk '{sum+=$1} END {print sum}')
printf "TOTAL = $totalone\n" >> $out_dir/$sample1.cpra.$type.diff


printf "File TWO:\n" >> $out_dir/$sample1.cpra.$type.diff
awk -F ':' '{print $5}' $out_dir/$sample2.2.cpra | sort | uniq -c >> $out_dir/$sample1.cpra.$type.diff
totaltwo=$(awk -F ':' '{print $5}' $out_dir/$sample2.2.cpra| sort | uniq -c | awk '{sum+=$1} END {print sum}')
printf "TOTAL = $totaltwo\n" >> $out_dir/$sample1.cpra.$type.diff

same=$(cat $out_dir/$sample1.1.cpra $out_dir/$sample2.2.cpra | cut -f1 |sort | uniq -cd | wc -l )
printf "\nMATCH = $same" >> $out_dir/$sample1.cpra.$type.diff
diff=$(($totalone-$totaltwo))
printf "\nMISMATCH = $diff\n" >> $out_dir/$sample1.cpra.$type.diff

oneonly=$(awk 'NR==FNR{a[$1];next}!($1 in a)' $out_dir/$sample2.2.cpra $out_dir/$sample1.1.cpra | wc -l)
twoonly=$(awk 'NR==FNR{a[$1];next}!($1 in a)' $out_dir/$sample1.1.cpra $out_dir/$sample2.2.cpra | wc -l)

printf "\nNumber of Variant(s) in ONE only: $oneonly\n" >> $out_dir/$sample1.cpra.$type.diff
printf "Number of Variant(s) in TWO only: $twoonly\n" >> $out_dir/$sample1.cpra.$type.diff

printf "\nVariant(s) in ONE only:\nChrom":"Pos":"Ref":"Alt":"GT\tSample\n" >> $out_dir/$sample1.cpra.$type.diff
awk 'NR==FNR{a[$1];next}!($1 in a)' $out_dir/$sample2.2.cpra $out_dir/$sample1.1.cpra >> $out_dir/$sample1.cpra.$type.diff
printf "\nVariant(s) in TWO only:\nChrom":"Pos":"Ref":"Alt":"GT\tSample\n" >> $out_dir/$sample1.cpra.$type.diff
awk 'NR==FNR{a[$1];next}!($1 in a)' $out_dir/$sample1.1.cpra $out_dir/$sample2.2.cpra >> $out_dir/$sample1.cpra.$type.diff
