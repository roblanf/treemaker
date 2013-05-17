

import logging
log = logging.getLogger("parser")

def get_aln_species(alnfile):
    """gets a species list and data count from a phylip alignment
       returns:
            * a simple list of species
            * a dictionary with species names as keys, amount of sequence data as values
            * a dictionary with genera as keys 
    
    """
    
    aln = open("/Users/Rob/Dropbox/Current_work/Lasantha/big_plants/big_plants.cn.phy", "r")

    header = aln.readline()    
    spp, sites = header.split()

#get a dictionary of names in the smith alignment, keyed by genus
smith_genera = {}
smith_data   = {}

for line in iter(smith_aln):
    species = line.split()[0]
    genus = species.split("_")[0] 
    l = smith_genera.setdefault(genus, [])
    l.append(species)
    smith_genera[genus] = l
    dna = line.split()[1]
    data = 9853 - dna.count("-")
    smith_data[species] = data
