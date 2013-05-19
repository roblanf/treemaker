
import species
import logging
log = logging.getLogger("input")

def get_input_spp(sppfile):
    
    spp = open(sppfile, "r").read().splitlines()
    input_species = {}
    
    for s in spp:
        s_clean = s.replace("_", " ")
        log.debug("Making species object for '%s'" %(s))
        input_species[s_clean] = species.Species(s_clean, s)
        
    return input_species
    
def get_aln_spp(alnfile):
    log.debug("Opening alignment '%s'" %(alnfile))
    
    aln = open(alnfile, "r")
    sites = int(aln.readline().split()[1])

    #get a dictionary of names in the smith alignment, keyed by genus
    aln_spp = {}        

    for line in iter(aln):
        name = line.split()[0]
        name_clean = name.replace("_", " ")
        dna = line.split()[1]
        data = sites - dna.count("-")
        s = species.Species(name_clean, name)
        s.data = data
        aln_spp[name_clean] = s

    return aln_spp