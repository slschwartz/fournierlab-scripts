#!/usr/bin/env python2.7
#coding: utf-8

import pandas as pd
import ete3
import re
import os, sys

ncbi     = ete3.NCBITaxa()
ranks = ['class', 'phylum', 'order', 'family', 'genus', 'superkingdom', 'kingdom']

if os.path.isdir(sys.argv[1]):
    print 'Input is a folder'

    tree_folder = sys.argv[1]
    for tree_file in os.listdir(tree_folder):
        if not tree_file.endswith('.treefile') and not tree_file.endswith('.tree'):
            continue
        print tree_file

        tree = ete3.Tree('%s/%s' %(tree_folder, tree_file), format=1)
        out  = open('%s/%s.figTree' %(tree_folder, tree_file), 'wb')
        out.write("#NEXUS\nbegin taxa;\n\tdimensions ntax=%i;\n\ttaxlabels\n" %len(tree))
        for node in tree.traverse():
            if node.is_leaf():
                taxon_name = node.name.split('|')[0].replace('Candidatus_', '')
                genus = taxon_name.split('_')[0]

                taxid = ncbi.get_name_translator([genus])
                if not taxid:
                    out.write('\t%s\n' %(node.name))
                    continue
                taxid = taxid.values()[0][0]

                lineage = {j: i for i, j in ncbi.get_rank(ncbi.get_lineage(taxid)).items()}
                lineage_names = ncbi.get_taxid_translator(lineage.values())

                out.write('\t%s ' %(node.name))
                comment = []
                for rank in ranks:
                    if rank in lineage:
                        comment.append('tax_%s="%s"' %(rank, lineage_names[lineage[rank]]))
                out.write('[&%s]\n' %' '.join(comment))

        newick_text = tree.write(format=0)
        out.write(';\nend;\n')
        out.write('begin trees;\n\ttree tree_1 = [&R] %s\nend;' %newick_text)
        out.close()

else:
    print 'Input is a tree file'
    #
    # single tree
    tree_folder = '.'
    tree_file   = sys.argv[1]
    tree = ete3.Tree('%s/%s' %(tree_folder, tree_file), format=1)
    out  = open('%s/%s.figTree' %(tree_folder, tree_file), 'wb')
    out.write("#NEXUS\nbegin taxa;\n\tdimensions ntax=%i;\n\ttaxlabels\n" %len(tree))
    branch_names = {}
    for node in tree.traverse():
        if node.is_leaf():
            taxon_name = node.name.split('|')[0].replace('Candidatus_', '')
            genus = taxon_name.split('_')[0]

            taxid = ncbi.get_name_translator([genus])
            if not taxid:
                out.write('\t%s\n' %(node.name))
                continue
            taxid = taxid.values()[0][0]

            lineage = {j: i for i, j in ncbi.get_rank(ncbi.get_lineage(taxid)).items()}
            lineage_names = ncbi.get_taxid_translator(lineage.values())

            out.write('\t%s ' % (node.name))
            comment = []
            for rank in ranks:
                if rank in lineage:
                    comment.append('tax_%s="%s"' % (rank, lineage_names[lineage[rank]]))
            out.write('[&%s]\n' %' '.join(comment))

    newick_text = tree.write(format=0)
    out.write(';\nend;\n')
    out.write('begin trees;\n\ttree tree_1 = [&R] %s\nend;' %newick_text)
    out.close()
