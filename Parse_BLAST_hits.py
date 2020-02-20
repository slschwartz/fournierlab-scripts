#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
# pandas is the python data package you need to use, naming it under call 'pd' here
# os has you import the working directory to this python workspace.


# In[ ]:


header = ['query acc.ver', 'subject acc.ver', '% identity',
          'alignment length', 'mismatches', 'gap opens', 
          'q. start', 'q. end', 's. start', 's. end', 'evalue',
          'bit score', 'subject tax id']
# this setup inserts a header set for your tab-delineated blast output file, which will be auto-incorp for the next steps


# In[ ]:


df = pd.read_table('RedA1.bls',sep='\t', comment='#',
                   header=None, names=header)

df['coverage %'] = (df['q. end'] - df['q. start'] + 1) / 334.
df = df[((df['% identity'] >= 70)&
        (df['coverage %'] >= 0.95))]
print ("Thresholds set, searching data...")

# this makes a new data column in the output, "coverage percent," which indicates query coverage in the hit.
# sets thresholds
# USER-DEFINED VARIABLE: the sequence length of query hit. Could add a column for sequence length and remove hard coding. 


# In[ ]:


for query_name in df['query acc.ver'].unique():
    tmp_df = df[df['query acc.ver'] == query_name].copy()
    out = open('RedA1.hit_ids', 'w')
    out.write('\n'.join(tmp_df['subject acc.ver'].unique()))
    # writes CORRESPONDING unique HITS for each BLAST query, given the established thresholds 
    # \n is inserting a line break between each element in the array, so that each sequence ID is line-separated
    out.close()
    os.system('blastdbcmd -db /home/sschwartz/sschwartz/UniRef90/uniref90.fasta -entry_batch RedA1.hit_ids > RedA1_recruited_hits')
    # last step is the final step of indexing. It syncs the IDs in your list with their info in the BLAST db. 
    # comment out any breaks in the loop if you want to iterate through your whole list.
print ("All done, check outfile")

