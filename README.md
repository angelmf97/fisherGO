# fisherGO

This programme is used to determine the enriched annotation terms within a list of genes, using the Fisher's exact test with the Bonferroni correction. Given the annotated genome (GO, IPRO or KEGG) of the organism and a list of selected genes, the programme creates .xlsx files containing the enriched terms with their description and p-values.


# Usage

Please, execute
``` 
fisherGO.py -h
```
or
```
sonar.py --help
```
for usage instructions.

Usage:
```
fisherGO.py [-h] [-a] -l  -t  [...]
```

The commands available are the following ones:

|        Command        |                                Function                               |
|-----------------------|-----------------------------------------------------------------------|
| -h, --help            | show the help message and exit.                                      |
| -a, --alpha           | desired alpha for the Fisher's exact test. Its default value is 0.05. |
| -l, --list            | list of genes to analyse.                                             |
| -t[ ...], --tab[ ...] | annotated genome(s).                                                  |

Usage example:
```
fisherGO.py -a 0.01 -l example.fasta -t go.tab ipro.tab kegg.tab
```
The example files can be found in this GitHub repository.

