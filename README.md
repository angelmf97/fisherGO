# fisherGO

This programme is used to determine the enriched annotation terms within a list of genes, using the Fisher's exact test with the Bonferroni correction. Given the annotated genome (GO, IPRO or KEGG) of the organism, a list of selected genes, and a set of genes to compare them with, the programme creates .xlsx files containing the enriched terms with their description and p-values.


# Usage

Please, execute
``` 
fisherGO.py -h
```
or
```
fisherGO.py --help
```
for usage instructions.

Usage:
```
fisherGO.py fisherGO.py [-h] [-a] -l  -s  -t  [...] [-o]
```

The commands available are the following ones:

| Command                   | Function                                                                                           |
|---------------------------|----------------------------------------------------------------------------------------------------|
| -h, --help                | show this help message and exit.                                                                   |
| -a , --alpha              | desired alpha for the Fisher's exact test. Its default value is 0.05                               |
| -l , --list               | list of genes/proteins of interest, in FASTA format                                                |
| -s , --set                | group of genes/proteins to compare the genes of interest with, in FASTA format                     |
| -t  [ ...], --tab  [ ...] | annotated genome(s)/proteome(s)                                                                    |
| -o , --output             | optional output file name (relative or absolute path). The .xlsx extension is added automatically. |

Usage example:
```
fisherGO.py -a 0.01 -l example.fasta -t go.tab ipr.tab kegg.tab
```
The example files can be found in this GitHub repository.

