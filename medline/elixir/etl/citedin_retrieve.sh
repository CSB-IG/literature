
# extracts pmids of articles that cite pbid=12807958
# prints out a coma separated value list, as specified by pubmed_citedin.xsl

PMID=$1

xsltproc --novalid pubmed_citedin.xsl "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?id=${PMID}"

