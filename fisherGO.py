#!/usr/bin/python
import re
import fisher
import xlsxwriter
import argparse



parser=argparse.ArgumentParser(description='This programme is used to find the enriched annotation terms within a list of genes/proteins, given the annotated genome/proteome of the organism. It works with GO, IPRO and KEGG annotations. The annotations must be written in the format used by the JGI (Joint Genome Institute).')
parser.add_argument('-a','--alpha',type=float,metavar='', default=0.05,help='desired alpha for the Fisher\'s exact test. Its default value is 0.05')
parser.add_argument('-l','--list',type=argparse.FileType('r'),metavar='',required=True,help='list of genes/proteins of interest, in FASTA format')
parser.add_argument('-s','--set',type=argparse.FileType('r'),metavar='',required=True,help='group of genes/proteins to compare the genes of interest with, in FASTA format')
parser.add_argument('-t','--tab',type=argparse.FileType('r'),metavar='',nargs='+',required=True,help='annotated genome(s)/proteome(s)')
parser.add_argument('-o','--output',type=str,metavar='',default='enrichment',required=False,help='optional output file name (relative or absolute path). The .xlsx extension is added automatically')

args=parser.parse_args()

def main():
    outname=args.output.replace('.xlsx','')
    workbook = xlsxwriter.Workbook(outname+'.xlsx')

    print '\n'
    print 'Performing the functional enrichment analysis, please wait.'
    print '\n'
    
    subsetIDs=re.findall('>.+\|.+\|(.+)\|',args.list.read())
    selected_total=len(subsetIDs)
    args.list.seek(0)
    
    setIDs=re.findall('>.+\|.+\|(.+)\|',args.set.read())
    total_proteins=len(setIDs)
    
    for annotated in args.tab:

        dictionary={}
        descriptions={}
        pathways={}
        header=annotated.readline()

        #This statements determine the type of annotation terms
        if 'gotermId' in header:
            x=3
            y=2
            type='GO'
            re_term=re.compile('([^\t]+)\t[^\t]+\t([^\t]+)\t[^\t]+\t([^\t]+)\n')

        elif 'ecNum' in header:
            x=2
            y=3
            type='KEGG'
            re_term=re.compile('([^\t]+)\t([^\t]+)\t([^\t]+)\t[^\t]+\t[^\t]+\t[^\t]+\t([^\t]+)\s')

        elif 'iprId' in header:
            x=2
            y=3
            type='IPR'
            re_term=re.compile('([^\t]+)\t([^\t]+)\t([^\t]+)\t[^\t]+\t[^\t]+\s')

        else:
            print 'Not supported file format. This programme only works for the annotation format of the Joint Genome Institute (JGI)'
            quit()

        #This loop creates a dictionary with annotation terms as keys and protein IDs as entries

	
        for line in annotated: 
            
	    terms=re_term.search(line)
	              
            if terms:
	    	if terms.group(1) not in setIDs:
		    continue 
                key=terms.group(x)
                entry=terms.group(1)
                desc=terms.group(y)

                if type=='KEGG':
                    path=terms.group(4)

                if key in dictionary:
                    if entry in dictionary[key]:
                        continue
                    else:
                        dictionary[key].append(entry)
                else:
                    dictionary[key]=[entry]
                    descriptions[key]=desc
                    if type=='KEGG':
                        pathways[key]=path

        #This block of code writes the .xlsx output file
        sheet=workbook.add_worksheet(type+' enriched terms')
        enriched_terms=[]
        not_enriched_terms=0
        nonselected_total=total_proteins-selected_total
        str=args.list.read()
        row=0
        col=0

        if type=='KEGG':

            sheet.write(row,col,'Term')
            sheet.write(row,col+1,'Description')
            sheet.write(row,col+2,'Pathway')
            sheet.write(row,col+3,'Number of proteins')
            sheet.write(row,col+4,'Protein IDs')
            sheet.write(row,col+5,'p-value')

        else:

            sheet.write(row,col,'Term')
            sheet.write(row,col+1,'Description')
            sheet.write(row,col+2,'Number of proteins')
            sheet.write(row,col+3,'Protein IDs')
            sheet.write(row,col+4,'p-value')

        row+=1

        for key in dictionary:

            selected_property=0
            nonselected_property=0

            for entry in dictionary[key]:
                re_jgi=re.compile('(>jgi\|.+\|('+entry+')\|)')
                search=re_jgi.search(str)

                if search:
                    selected_property+=1

                else:
                    nonselected_property+=1

            selected_noproperty=selected_total-selected_property

            nonselected_noproperty=nonselected_total-nonselected_property

            p=fisher.pvalue(selected_property,selected_noproperty,nonselected_property,nonselected_noproperty)

            if p.right_tail<=args.alpha/len(dictionary):
                enriched_terms.append(key)
                sheet.write(row,col,key)
                sheet.write(row,col+1,descriptions[key])
                proteinIDs=''
                flag=0

                for n in dictionary[key]:
                    if flag==0:
                        proteinIDs+=n
                        flag=1
                    else:
                        proteinIDs+=(', '+n)


                if type=='KEGG':
                    sheet.write(row,col+2,pathways[key])
                    sheet.write(row,col+3,selected_property)
                    sheet.write(row,col+4,proteinIDs)
                    sheet.write(row,col+5,p.right_tail)

                else:
                    sheet.write(row,col+2,selected_property)
                    sheet.write(row,col+3,proteinIDs)
                    sheet.write(row,col+4,p.right_tail)
                row+=1

            else:
                not_enriched_terms+=1
                continue

        args.list.seek(0)

        print type, 'terms enrichment analysis.'
        print '-'*25
        print 'Enriched terms:', len(enriched_terms)
        print 'Not enriched terms:', not_enriched_terms
        print 'Total terms analysed:', len(dictionary)
        print '\n'

    workbook.close()


if __name__=='__main__':

    main()
