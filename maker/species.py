
import genbank
import tnrs

import logging
logging.basicConfig(level="INFO")

class Species(object):
    """A Species file
    """

    def __init__(self, name):
        self.name = name
        self.genus = self.name.split()[0]
        self.species = self.name.split()[1]
        self.binomial = " ".join([self.genus, self.species])
        
        # use the TNRS to get a name        
        self.tnrs_response = tnrs.check_one_species(self.binomial)
        if self.tnrs_response != "NA":
            self.tnrs_acceptedname = tnrs.get_acceptedname(self.tnrs_response)
            
            if self.tnrs_acceptedname != self.name:
                logging.warning("Species name '%s' is different from the TNRS name '%s'."
                                " Please check for spelling mistakes." %(self.name, self.tnrs_acceptedname))
            
        else:
            self.tnrs_acceptedname = "NA"

        # use GenBank get a name
        
        # try a few things to get a taxonID:
        self.taxid = genbank.get_taxid(self.name)

        if self.taxid == "NA":
            logging.info("Couldn't find TaxonID for '%s'" % self.name)
        
            if self.binomial != self.name:
                taxid2 = genbank.get_taxid(self.binomial)
            else:
                taxid2 = "NA"
            
            if self.tnrs_acceptedname != self.name and self.tnrs_acceptedname != "NA":
                taxid3 = genbank.get_taxid(self.tnrs_acceptedname)
            else:
                taxid3 = "NA"
        
            if taxid2 == "NA" and taxid3 != "NA":  
                logging.warning("Found TaxonID using TNRS name '%s', please check" %(self.tnrs_acceptedname))
                self.taxid = taxid3
            elif taxid3 == "NA" and taxid2 != "NA":  
                logging.warning("Found TaxonID using binomial '%s', please check" %(self.binomial))
                self.taxid = taxid2
            else:
                logging.info("Checked TNRS and binomial but still couldn't find TaxonID")
                
        if self.taxid != "NA":
            self.lineage = genbank.get_lineage(self.taxid)
            self.genbank_binomial = " ".join([self.lineage['genus'], 
                                              self.lineage['species']])
        else:
            self.lineage = "NA"
            self.genbank_binomial = "NA"

        nameset = set([self.name, self.binomial, self.genbank_binomial, self.tnrs_acceptedname])
        if 'NA' in nameset: nameset.remove('NA')
        
        self.nameset = nameset
        
        logging.info("Created %s", self)
    
    def __str__(self):
        return self.name


if __name__ == "__main__":

    a = Species("Eucalyptos globulus")
    
    print(a)
    
    print a.name
    print a.genus
    print a.species
    print a.binomial
    print a.taxid
    print a.lineage
    print a.genbank_binomial
    print a.tnrs_acceptedname
    print a.nameset
    

         
