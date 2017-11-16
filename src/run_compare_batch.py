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

samplelist = ConfigSectionMap("List")['pair']
if os.path.isfile(samplelist):
    print ("SAMPLE LIST: {} EXISTS.".format(samplelist))
else:
    print ("SAMPLE LIST: {} DOES NOT EXISTS.".format(samplelist))
    sys.exit()

# variables
run_dir = ConfigSectionMap("Dir")['run_dir']
vcf1    = ConfigSectionMap("Vcf")['vcf1']
vcf2    = ConfigSectionMap("Vcf")['vcf2']
vcf_dir = os.path.join(run_dir,"vcf")
snp_out_dir = os.path.join(run_dir,"outputsnp")
indel_out_dir = os.path.join(run_dir,"outputindel")
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
def CompareCPRA(type,out_dir,sub):
    with open(samplelist) as f:
        for line in f:
            line = line.strip()
            sample1,sample2 = line.split('\t')
            cmd = ("bash compareCPRA.sh {} {} {} {} {} {}".format(sample1,sample2,vcf_dir,out_dir,type,sub))
            subprocess.call(cmd, shell=True, executable='/bin/bash')



print("Print_vcf STARTS")
print("Printing vcf..")
#Print_vcf()
print("Print_vcf ENDS")

print("CompareCPRAsnp STARTS")
print("Comparing SNPs..")
#CompareCPRA(snp,snp_out_dir,'snp')
print("CompareCPRA snp ENDS")

print("CompareCPRAindel STARTS")
print("Comparing INDELs..")
#CompareCPRA(indel,indel_out_dir,'indel')
print("CompareCPRA indel ENDS")

if not os.path.exists("summary"):
    os.makedirs("summary")

#os.system('python batchsummary.py')
print("batchsymmary done")
#os.system('python genecount.snp.py')
print("genecount.snp done")
#os.system('python genecount.indel.py')
print("genecount.indel done")

print("batchgenecount.py starts")
os.system('python batchgenecount.py')
print("batchgenecout.py ENDS")
