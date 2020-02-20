#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import os
get_ipython().run_line_magic('cd', '~/Desktop/')
# pandas is the python data package you need to use, naming it under call 'pd' here
# os has you import the working directory to this python workspace.

#This script is ONE OF TWO that must be run to get the full sequences downloaded. This can be paired with an array shell file, and second dbcmd file can be paired with a second array shell file to give automated fasta hits. 



header = ['query acc.ver', 'subject acc.ver', '% identity',
          'alignment length', 'mismatches', 'gap opens', 
          'q. start', 'q. end', 's. start', 's. end', 'evalue',
          'bit score','taxid']
# this setup inserts a header set for your tab-delineated blast output file, which will be auto-incorp for the next steps



df = pd.read_table('cytocA_ncbihits', sep='\t', comment='#',
                   header=None, names=header)

len(df)
#sanity check


df = df[df['evalue']<= 1.0e-4]
# this makes a new data column in the output, "coverage percent," which indicates query coverage in the hit.
# sets thresholds
# USER-DEFINED VARIABLE: the sequence length of query hit. Should add a column for sequence length and remove hard coding


len(df)


for query_name in df['query acc.ver'].unique():
    tmp_df = df[df['query acc.ver'] == query_name].copy()
    out = open('outgroupsearch_cytocA_ncbi.hit_ids', 'w')
    out.write('\n'.join(tmp_df['subject acc.ver'].unique()))
    # writes CORRESPONDING unique HITS for each BLAST query, given the established thresholds 
    # \n is inserting a line break between each element in the array, so that each sequence ID is line-separated
    #USER-DEFINED VARIABLE: Filename
    out.close()
print("All done, check for hits, run dbcmd and then rename if needed")




