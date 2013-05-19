
import genbank
import tnrs
import json

import logging
log = logging.getLogger("species")

class Species(object):
    """A Species file
    """

    def __init__(self, clean_name, original_name):
        log.info("Starting new species: '%s'" % original_name)

        self.clean_name = clean_name
        self.original_name = original_name
        self.original_binomial = self.make_binomial()
        self.tnrs_acceptedname = None
        self.tnrs_binomial = None
        self.tnrs_genus = None
        self.genbank_name = None
        self.genbank_binomial = None
        self.genbank_genus = None
        self.data = None
    
    def __str__(self):
        return self.original_name
    
    def make_binomial(self):
        items = self.clean_name.split()
        if len(items)>1:
            binomial = ' '.join([items[0], items[1]])
        else:
            binomial = ' '.join([items[0], "spp"])
        return binomial

    @property
    def binomial(self):
        if hasattr(self, '_binomial'):
            return self._binomial
        else:
            checked_binomial = self.set_binomial(self.clean_name)
            self._binomial = checked_binomial
            return self._binomial

    @property
    def original_genbank_binomial(self):
        if hasattr(self, '_original_genbank_binomial'):
            return self._original_genbank_binomial
        else:
            original_genbank_binomial = self.get_genbank_binomial(self.original_binomial)
            self._original_genbank_binomial = original_genbank_binomial
            return self._original_genbank_binomial

    @property
    def tnrs_genbank_binomial(self):
        if hasattr(self, '_tnrs_genbank_binomial'):
            return self._tnrs_genbank_binomial
        else:
            tnrs_genbank_binomial = self.get_genbank_binomial(self.binomial)
            self._tnrs_genbank_binomial = tnrs_genbank_binomial
            return self._tnrs_genbank_binomial

    
    def get_genbank_binomial(self, binomial):
        taxid = self.get_taxonID(binomial)
        if taxid != "NA":
            lineage = genbank.get_lineage(taxid)
            genbank_binomial = " ".join([lineage['genus'], lineage['species']])
        else:
            self.lineage = "NA"
            genbank_binomial = "NA"
        
        log.debug("genbank_binomial is: '%s'" % genbank_binomial)
        return genbank_binomial
    
    
    def set_binomial(self, name):
        log.debug("Checking spelling of '%s'" %(name))
        genus = self.clean_name.split()[0]
        species = self.clean_name.split()[1]
        binomial = " ".join([genus, species])
        
        self.tnrs_acceptedname = tnrs.check_one_species(binomial)
        tnrs_split = self.tnrs_acceptedname.split()
        
        if len(tnrs_split)>1:
            self.tnrs_binomial = ' '.join([tnrs_split[0], tnrs_split[1]])
        else:
            self.tnrs_binomial = self.tnrs_acceptedname

        if binomial == self.tnrs_binomial:
            checked_binomial = binomial
            self.TNRSmatch = "perfect"
            log.debug("Binomial matches TNRS")

        elif binomial != self.tnrs_binomial and self.tnrs_binomial != "NA" and len(self.tnrs_binomial.split())>1:
            log.warning("Spelling error detected. Binomial '%s' doesn't match TNRS "
                            "'%s'" %(binomial, self.tnrs_binomial))
            checked_binomial = self.tnrs_binomial
            self.TNRSmatch = "imperfect"

        else:
            log.debug("Binomial '%s' not found on TNRS. Please check" %(name))

            log.debug("Checking genus name only against TNRS...")
            tnrs_genus = tnrs.check_one_species(genus)

            if tnrs_genus == genus:
                log.debug("Genus matches tnrs")
                checked_binomial = ' '.join([tnrs_genus, species])
                self.TNRSmatch = "genus"
                
            elif tnrs_genus != genus and tnrs_genus != "NA":
                log.warning("Genus spelling error detected: input '%s' "
                                "doesn't match TNRS '%s', please check" %(genus, tnrs_genus))
                checked_binomial = ' '.join([tnrs_genus, species])
                self.TNRSmatch = "genus_imperfect"
            else:
                log.warning("No genus match found for '%s', please check" % genus)
                self.TNRSmatch = "none"
                checked_binomial = binomial

        log.info("Original binomial is    : '%s'" %(self.original_binomial))                
        log.info("Spellchecked binomial is: '%s'" %(checked_binomial))
        
        return checked_binomial           
        
    def set_genbank_name(self, name):
        self.set_taxonID(name)
        if self.taxid != "NA":
            self.lineage = genbank.get_lineage(self.taxid)
            self.genbank_binomial = " ".join([self.lineage['genus'], 
                                              self.lineage['species']])
        else:
            self.lineage = "NA"
            self.genbank_binomial = "NA"
        
        log.info("set genbank_binomial to: '%s'" %self.genbank_binomial)
        
         
    def get_taxonID(self, name):
        taxid = genbank.get_taxid(name)
        return taxid
            
    def set_taxonID(self, name):

        taxids = {}
        nameset = set([self.name, self.binomial, self.tnrs_acceptedname, self.tnrs_binomial])
        if 'NA' in nameset: nameset.remove('NA')
        
        for name in nameset:
            taxid = genbank.get_taxid(name)
            taxids[name] = taxid
        
        taxid_set = set(taxids.values())
        if 'NA' in taxid_set: taxid_set.remove('NA')

        if len(taxid_set)>1:
            out = json.dumps(taxids, indent=2)
            log.warning("More than one taxon ID found: \n%s" %taxids)
            self.taxid = "NA"
            log.info("TaxonID set to 'NA'")
        if len(taxid_set)==1:
            self.taxid = list(taxid_set)[0]
            log.info("TaxonID set to %s" % self.taxid)
        if len(taxid_set)==0:
            log.warning("No taxon ID found")
            self.taxid = "NA"
            log.info("TaxonID set to 'NA'")
                    


if __name__ == "__main__":

    a = Species("Eucalyptos globulus")
            

         
