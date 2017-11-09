#!/home/jeffrey/miniconda3/bin/python

import numpy as np
import pandas as pd
import glob
import os
from pandas.io.common import EmptyDataError
import configparser
import logging


configfile = 'config_batch.ini'
Config = configparser.ConfigParser()
Config.read(configfile)
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try: 
            dict1[option] = Config.get(section,option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


samplelist = ConfigSectionMap("List")['pair']
#samplelist = "sample.list"

dictfile = "dictionary.txt"
dir = "summary/"

# use prepared CPRA|GENE superset as dictionary
def genedict1():
    superdict = pd.read_csv(dictfile,sep='\t')
    superdict.set_index("CHROM:POS:REF:ALT",drop=True,inplace=True) 
    dict =superdict.to_dict()
    #print(dict)
    return dict

# import files and preprocess
def comparecpra(dictionary,type):
    with open(samplelist) as f:
        list_df1 = []
        list_df2 = [] 
        for line in f:
            line = line.strip()
            global sample1
            global sample2
            sample1,sample2 = line.split()
            global f1
            global f2
            
            try:
                f1 = pd.read_csv('output'+type+'/'+sample1+'.1.cpra',sep='\t',header=None)
                f2 = pd.read_csv('output'+type+'/'+sample2+'.2.cpra',sep='\t',header=None)
                f1[2]=f1[0].str.split(':').str[:4].apply(lambda x: ':'.join(x))
                f2[2]=f2[0].str.split(':').str[:4].apply(lambda x: ':'.join(x))
                print(f1)
                print(f2)
                f1['FP']=f1[0].isin(f2[0])
                f1['gene'] = f1[2].map(dictionary["Gene.knowngene"])
                f2['FN']=f2[0].isin(f1[0])
                f2['gene'] = f2[2].map(dictionary["Gene.knowngene"])
                print(f1)
                print(f2)
            except EmptyDataError:
                f1 = pd.DataFrame(columns=['0','1','2','FP','gene'])
            
                f2 = pd.DataFrame(columns=['0','1','2','FN','gene'])

            list_df1.append(f1)
            list_df2.append(f2)
        df1comb = pd.concat(list_df1)
        df2comb = pd.concat(list_df2)
        df1comb.to_csv(dir+'combined1.'+type+'.txt', sep='\t')
        df2comb.to_csv(dir+'combined2.'+type+'.txt', sep='\t')
    return df1comb,df2comb


# print count table
def counttable(f1,f2,type):
    # count of Total
    Total = f1.groupby('gene').count()['FP']
    Totaldf = pd.DataFrame(Total)
    Totaldf.rename(columns={'FP':'Total'},inplace=True)
    # count of TP
    TP = f1.groupby('FP').get_group(True).groupby('gene').count()['FP']
    TPdf = pd.DataFrame(TP)
    TPdf.rename(columns={'FP':'TP'},inplace=True)
    # count of FP
    FP = f1.groupby('FP').get_group(False).groupby('gene').count()['FP']
    FPdf = pd.DataFrame(FP)
    FPdf.rename(columns={'FP':'FP'},inplace=True)
    # count of FN
    FN = f2.groupby('FN').get_group(False).groupby('gene').count()['FN']
    FNdf = pd.DataFrame(FN)
    FNdf.rename(columns={'FN':'FN'},inplace=True)
    #FNdf['FN'] = FNdf['FN'].astype(str).astype(int)

    results = pd.concat([Totaldf,TPdf,FPdf,FNdf],axis=1).fillna(value=0)
    results[['FP','FN']] = results[['FP','FN']].astype(int)
    print(results)
    results.to_csv(dir+'genecounttable.'+type+'.txt', sep='\t')

# RUN
#genedict()
dict = genedict1()
comparecpra(dict,'snp')
comparecpra(dict,'indel')
print("gene dictionary created")


#try:
#    comparecpra()
#except:
#    pass
try:
    df1comb,df2comb = comparecpra(dict,'snp')
except:
    pass

counttable(df1comb,df2comb,'snp')



try:
    df1comb,df2comb = comparecpra(dict,'indel')
except:
    pass


#print(df1comb)
counttable(df1comb,df2comb,'indel')
