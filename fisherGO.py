#!/usr/bin/python
import re
import fisher
import xlsxwriter
import argparse



parser=argparse.ArgumentParser(description='This programme is used to find the enriched annotation terms within a list of proteins, given the annotated proteome of the organism. It works with GO, IPRO and KEGG annotations.')
parser.add_argument('-a','--alpha',type=float,metavar='', default=0.05,help='desired alpha for the Fisher\'s exact test. Its default value is 0.05.')
parser.add_argument('-l','--list',type=argparse.FileType('r'),metavar='',required=True,help='list of proteins to analyse.')
parser.add_argument('-t','--tab',type=argparse.FileType('r'),metavar='',nargs='+',required=True,help='annotated proteome(s).')
parser.add_argument('-o','--output',type=str,metavar='',default='enrichment.xlsx',nargs=1,required=False,help='optional output file name (relative or absolute path).')

args=parser.parse_args()

def main():

    workbook = xlsxwriter.Workbook(args.list.name+'_enrichment.xlsx')

    print '\n'

    total_proteins=0
    selected_total=0

    for line in args.list:
        re_list=re.compile('>jgi\|.+')
        search=re_list.search(line)
        if search:
            selected_total+=1
    args.list.seek(0)

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
                key=terms.group(x)
                entry=terms.group(1)
                desc=terms.group(y)

                if type=='KEGG':
                    path=terms.group(4)
                total_proteins+=1

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
