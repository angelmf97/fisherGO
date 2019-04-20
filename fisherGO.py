from sys import argv
import re
import fisher
import xlsxwriter

workbook = xlsxwriter.Workbook(argv[2]+'_enrichment.xlsx')
annotated=open(argv[1])
dictionary={}
total_proteins=0
#regex for interproterms
re_GO=re.compile('([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)')
#This loops creates a dictionary with InterProterms as keys and protein IDs as entries
for line in annotated:
    terms=re_GO.search(line)
    if terms:
        key=terms.group(2)
        entry=terms.group(1)
        total_proteins+=1
        if key in dictionary:
            if entry in dictionary[key]:
                continue
            else:
                dictionary[key].append(entry)
        else:
            dictionary[key]=[entry]

enriched_sheet=workbook.add_worksheet('Enriched terms')
not_enriched_sheet=workbook.add_worksheet('Not enriched terms')
enriched_terms=[]
not_enriched_terms=[]
selected_names=open(argv[2])
selected_total=len(selected_names.readline())
nonselected_total=total_proteins-selected_total
str=selected_names.read()
row=0
col=0
enriched_sheet.write(row,col,'Term')
enriched_sheet.write(row,col+1,'p-value')
row+=1
not_row=0
not_col=0
not_enriched_sheet.write(not_row,not_col,'Term')
not_enriched_sheet.write(not_row,not_col+1,'p-value')
not_row+=1
for key in dictionary:
    selected_property=0
    selected_noproperty=0
    nonselected_property=0
    nonselected_noproperty=0
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
    if p.right_tail<=0.05/len(dictionary):
        enriched_terms.append(key)
        enriched_sheet.write(row,col,key)
        enriched_sheet.write(row,col+1,p.right_tail)
        row+=1
    else:
        enriched_terms.append(key)
        not_enriched_sheet.write(not_row,not_col,key)
        not_enriched_sheet.write(not_row,not_col+1,p.right_tail)
        not_row+=1

workbook.close()
print 'Not enriched terms:', len(not_enriched_terms)
for term in not_enriched_terms:
    print term

print 'Enriched terms:', len(enriched_terms)
for term in enriched_terms:
    print term

print 'Total terms analysed:', len(dictionary)
