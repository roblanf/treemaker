import logging
import matches

logging.basicConfig(
    format="%(levelname)-8s | %(asctime)s | %(message)s",
    level=logging.INFO
)


def main(sppfile, alnfile):
    
    # this is a list of tuples which will hold our results: (input_name, tree_name)
    results = []

    # first we get simple lists of species in each input file
    tree_spp = get_aln_species(alnfile)
    input_spp = get_input_spp(sppfile)
    
    # now we look for exact matches. These are easy.
    # we do this now because we can then reduce the amount of hard work we do later
    results = get_exact_matches(tree_spp, input_spp)
    
    # next we use different services to match possible names
    tree_dict = get_species_possibilities(tree_sppp, services = 'genbank')
    input_dict = get_species_possibilities(tree_spp,  services = 'genbank')
    