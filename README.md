# Interactome Filter
A script remove from a *general interactome* specific genes (nodes) based on their expression value. This can be used to highlight differences among genes expressed in different tissues or cell types.

Data of gene expression can be downloaded from the Human Protein Atlas (HPA). Their datasets include expression levels of genes based on RNA-seq: TPM, pTPM and nTPM ([normalized expression](https://www.proteinatlas.org/about/assays+annotation#normalization_rna), NX).

## Requirements
 python (3.5 or above) and [numpy](https://numpy.org/install/)

## Usage 
 The script requires at least two arguments: 
 
 - *Interactome file* formatted as a list of edges
 - *Gene expression file* a two-column file with genes (for a particular tissue or cell type) and their expression value.

The program will create a *filtered interactome* with the genes from the *gene-expression_file* that have an expression value &ge; 1. This value can be changed using the *--cutoff* option:
 
		python3 interactome_filter.py interactome_file gene-expression_file -o expressionfiltered-interactome_file.tsv

Check the *Example* section to see a case of use

## Example
Filter a general interactome using the normalized expression values from the *RNA HPA tissue gene data* file from the [Human Protein Atlas](https://v20.proteinatlas.org/about/download): [*rna_tissue_hpa.tsv.zip*](https://v20.proteinatlas.org/download/rna_tissue_hpa.tsv.zip).

The general interactome used in this example was downloaded from BioGrid[https://downloads.thebiogrid.org/BioGRID] and only includes physical interactions of human proteins.

Note that the file downloaded from the HPA includes one single TSV with different expression values for all tissues. Here, *gen_tissue-expression_files.sh* is used to generate the files in the format that is expecting the interactome filter (two columns with genes and expression values for a single tissue or cell type).

		bash gen_tissue-expression_files.sh rna_tissue_hpa.tsv.zip tissue-filtered_interactomes/
		python3 interactome_filter.py biogrid_hsa-oss_phys.tsv.gz adipose_tissue.tsv -o biogrid_hsa-oss_phys_adipose_tissue.tsv

## References
- [Human Protein Atlas](https://www.proteinatlas.org)
- Uhlén M et al., **Tissue-based map of the human proteome**. *Science* (2015) DOI: [10.1126/science.1260419](http://doi.org/10.1126/science.1260419)
- Chris Stark, Bobby-Joe Breitkreutz, Teresa Reguly, Lorrie Boucher, Ashton Breitkreutz, Mike Tyers, **BioGRID: a general repository for interaction datasets**, *Nucleic Acids Research*, Volume 34, Issue suppl_1, 1 January 2006, Pages D535–D539. DOI: [10.1093/nar/gkj109](https://doi.org/10.1093/nar/gkj109)
