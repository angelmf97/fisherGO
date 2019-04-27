# fisherGO

This programme is used to find the enriched annotation terms within a list of genes, given the annotated genome of the organism. It works with GO, IPRO and KEGG annotations.

# Usage

Please, execute
	fisherGO.py -h
or
	sonar.py --help
for usage instructions.

Usage:
	fisherGO.py [-h] [-a] -l  -t  [...]

The commands available are the following ones:
	-h, --help            		show this help message and exit
  	-a , --alpha          		desired alpha for the Fisher's exact test. Its default value is 0.05.
  	-l , --list           		list of genes to analyse.
  	-t  [ ...], --tab  [ ...]	annotated genome(s).


Usage example:
	fisherGO.py -a 0.01 -l example.fasta -t go.tab ipro.tab kegg.tab
The example files can be found in this GitHub repository.

