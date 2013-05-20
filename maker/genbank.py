
import logging
log = logging.getLogger("genbank")

import urllib
import urllib2
import re


def get_taxid(term):
    """get a taxid from entrez taxonomy, by searching with a name"""

    _toolname = 'get_taxid'
    _email = ""
    params = {
        'db': 'taxonomy',
        'tool': _toolname,
        'email': _email,
        'term': term,
        'rettype': 'xml',
    }
    url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
    url = url + urllib.urlencode(params)
    data = urllib.urlopen(url).read()
    try:
        taxid = re.search('<Id>(\S+)</Id>', data).group(1)
        log.debug("Got TaxonID for '%s': %s" %(term, taxid))
    except:
        taxid = 'NA'
        log.debug("No TaxonID found for '%s'" %term)
    return taxid

def get_lineage(TaxID):
    '''
    This function takes as input a genbank taxonID and returns a taxomony dictionary
    It only works if the TaxID is at the species level
    '''

    taxonomy = {'taxid': TaxID, 'phylum': 'NA', 'subphylum': 'NA', 'superclass': 'NA', 'class': 'NA', 'superorder': 'NA', 'order': 'NA', 'suborder': 'NA', 'family': 'NA', 'subfamily': 'NA', 'genus': 'NA'}

    if TaxID == "NA":
        taxonomy['species'] = 'NA'
        return taxonomy

    url = 'http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=%s&lvl=3&keep=0&srchmode=1&unlock&lin=f' %(TaxID)
    entrez_tax = urllib2.urlopen(url).read() #this is the dirty looking xml file from entrez
	
    #now extract all the lineage data from entrez_tax
    for level in taxonomy:
        m = re.search('"%s">(\S+)</a>' %(level), entrez_tax)
        try:
            taxonomy[level] = m.group(1)
        except:
            taxonomy[level] = "NA"
    try:
        binomial = re.search(r">Taxonomy browser ((.+))<", entrez_tax)
        binomial = binomial.group(1)[1:-1]
        species = binomial.split()[1]	
        taxonomy['species'] = species
    except:
        taxonomy['species'] = "NA"
	
	log.debug("Got lineage data for taxID %s" %(TaxID))
		
    return taxonomy


def get_genbank_binomial(species_name):
    """Enter a species name, return the binomial from genbank
       Sometimes useful because it can correct synonyms
    """

    taxid = get_taxid(s)
    lineage = get_lineage(taxid)
    genbank_binomial = " ".join([lineage["genus"], lineage['species']])

    return taxid, lineage
