#!/home/jeffrey/miniconda3/envs/myenv/bin/python

import configparser
import os
import subprocess
import logging
import sys
import os.path

configfile = 'config_batch.ini'
Config = configparser.ConfigParser()
Config.read(configfile)
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1



# read config file
if os.path.isfile(configfile):
    print ("CONFIG FILE: {} EXISTS.".format(configfile))
else:
    print ("CONFIG FILE: {} DOES NOT EXISTS.".format(configfile))
    sys.exit()

#samplelist = 'test_sample.list'
samplelist = ConfigSectionMap("List")['pair']
if os.path.isfile(samplelist):
    print ("SAMPLE LIST: {} EXISTS.".format(samplelist))
else:
    print ("SAMPLE LIST: {} DOES NOT EXISTS.".format(samplelist))
    sys.exit()

# variables
#sample  = ConfigSectionMap("Sample")['sample']
run_dir= ConfigSectionMap("Dir")['run_dir']
#print(run_dir)
#samplefile = ConfigSectionMap("List")['sample']
#print(samplefile)

vcf1    = ConfigSectionMap("Vcf")['vcf1']
vcf2    = ConfigSectionMap("Vcf")['vcf2']
#indv_vcf1= "vcf/"+sample+".1.vcf"
#indv_vcf2= "vcf/"+sample+".2.vcf"
#diff_opt= ConfigSectionMap("Vcftools")['diff_opt']
vcf_dir= os.path.join(run_dir,"vcf")
snp_out_dir= os.path.join(run_dir,"outputsnp")
indel_out_dir= os.path.join(run_dir,"outputindel")
snp = ConfigSectionMap("Type")['snp']
indel = ConfigSectionMap("Type")['indel']

# generate individual vcf
def Print_vcf():
    with open(samplelist) as f:
        for line in f:
            line = line.strip()
            sample1,sample2 = line.split('\t')
            cmd = ("bash print_vcf.sh {} {} {} {}".format(vcf1,vcf2,sample1,sample2))
            subprocess.call(cmd, shell=True, executable='/bin/bash')

# generate comparison
def CompareCPRAsnp():
    with open(samplelist) as f:
        for line in f:
         line = line.strip()
         sample1,sample2 =line.split('\t')
         cmd = ("bash compareCPRA.sh {} {} {} {} {} snp".format(sample1,sample2,vcf_dir,snp_out_dir,snp))
         subprocess.call(cmd, shell=True, executable='/bin/bash')

def CompareCPRAindel():
    with open(samplelist) as f:
        for line in f:
         line = line.strip()
         sample1,sample2 =line.split('\t')
         cmd = ("bash compareCPRA.sh {} {} {} {} {} indel".format(sample1,sample2,vcf_dir,indel_out_dir,indel))
         subprocess.call(cmd, shell=True, executable='/bin/bash')


# Not using this
def Print_mismatch():
    cmd = ("bash test_print_mismatch.sh")
    subprocess.call(cmd, shell=True, executable='/bin/bash')

# Vcftools is another option, which is not used for now.
def Vcftools():
	with open(samplelist) as f:
		for line in f:
		 line = line.strip()
		 sample1,sample2= line.split('\t')
		 indv_vcf1 = "vcf/"+sample1+".1.vcf"
		 indv_vcf2 = "vcf/"+sample2+".2.vcf"
		 print(indv_vcf1)
		 print(indv_vcf2)
		 cmd = ("bash compare_variants.sh {} {} {} {}"\
		 .format(indv_vcf1,indv_vcf2,diff_opt,sample1))

		 subprocess.call(cmd, shell=True, executable='/bin/bash')


print("Print_vcf STARTS")
print("Printing vcf..")
#Print_vcf()
print("Print_vcf ENDS")

print("CompareCPRAsnp STARTS")
print("Comparing SNPs..")
#CompareCPRAsnp()
print("CompareCPRAsnp ENDS")

print("CompareCPRAindel STARTS")
print("Comparing INDELs..")
#CompareCPRAindel()
print("CompareCPRAindel ENDS")

os.system('python printsummary.py')
#Vcftools() <-- another option
