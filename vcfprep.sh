#preprocess macrogen WGS vcf for comparison
vcfprefix=$1
targetbed=$2

#remove chr and reheader
bcftools view $vcfprefix.vcf.gz | awk '{gsub(/^chr/,""); print}' | awk '{ gsub(/\|/,"/",$0)}1' | bgzip -c > $vcfprefix.mod.vcf.gz
bcftools norm -m-both $vcfprefix.mod.vcf.gz | bcftools norm -f /home/database/b37/human_g1k_v37_decoy.fasta | awk '{gsub(/1\/0/,"0/1",$0)}1' | bgzip -c > $vcfprefix.split.vcf.gz
#awk '{gsub(/^chr/,""); print}' $vcfprefix.vcf.gz | bgzip -c > $vcfprefix.mod.vcf.gz
tabix -p vcf $vcfprefix.split.vcf.gz

#subset ROI
#bcftools view -R $targetbed $vcfprefix.split.vcf.gz -t "^X,Y,M" | bgzip -c > $vcfprefix.auto.vcf.gz
#tabix -p vcf $vcfprefix.auto.vcf.gz
