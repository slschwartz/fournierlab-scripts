# fournierlab-scripts

These scripts are designed for sequence collection and alignment, data curation, and treefile manipulations in the construction and optimization of phylogenetic trees. 

Cull Alignment File: To remove manually-curated taxa from a protein alignment.

Parse BLAST hits / Parse 'n Pull scripts: Input is tab-delineated BLAST output file. Allows filtering of hits (by coverage, percent identity, etc) and will pull corresponding unique hit IDs.

Rename Headers for Visualization: Renames BLAST-formatted FASTA headers to be compatible with downstream visualization scripts (e.g. Visualize in FigTree).

No Rain Delays: Removes double headers (duplicated taxon IDs for identical protein hits) from FASTA files without removing sequence data.

Tree Manips UDV: Uses ETE3 toolkit to overlay alignment/sequence features onto a tree. Allows for branch coloration by taxonomy. 


