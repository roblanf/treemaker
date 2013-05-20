import species
import inputparser
import tnrs
import matches
import copy

import logging

logging.basicConfig(level="INFO")
fmt = logging.Formatter("%(levelname)-8s | %(asctime)s | %(name)-10s | %(message)s")
logging.getLogger("").handlers[0].setFormatter(fmt)

log = logging.getLogger("main")


def main(sppfile, alnfile, match_genera=False):
    
    # first we get simple dict of species objects in the input file
    # each species is built as a species object, named by the actual name
    unmatched_input_spp = inputparser.get_input_spp(sppfile)
    log.info("Loaded %d species from input file" %len(unmatched_input_spp))
    
    # next we get a dict of spp in stephen smith's alignment, each one has
    # the amount of data in in the alignment for that spp too
    unmatched_aln_spp = inputparser.get_aln_spp(alnfile)
    
    # a dictionary keyed by input species, with alignment species as values
    matched_spp = {}
    
    # 1. Search for exact matches between input spp and smith spp    
    unmatched_input_spp, unmatched_aln_spp, matched_spp = matches.exact(unmatched_input_spp, unmatched_aln_spp, matched_spp)
    
    # 2. Search for exact original binomial matches between input spp and smith spp
    unmatched_input_spp, unmatched_aln_spp, matched_spp = matches.exact_binomial(unmatched_input_spp, unmatched_aln_spp, matched_spp, type="original")
    
    # 3. Now we try spelchecking the binomial of each input taxon and see if that helps
    unmatched_input_spp, unmatched_aln_spp, matched_spp = matches.exact_binomial(unmatched_input_spp, unmatched_aln_spp, matched_spp, type="spellchecked")
    
    # 4. Now we try getting input_binomial -> genbank_spp and see if that helps
    unmatched_input_spp, unmatched_aln_spp, matched_spp = matches.exact_binomial(unmatched_input_spp, unmatched_aln_spp, matched_spp, type="original_genbank")
    
    # 5. Finally we try tnrs_binomial -> genbank_spp and see if that helps
    unmatched_input_spp, unmatched_aln_spp, matched_spp = matches.exact_binomial(unmatched_input_spp, unmatched_aln_spp, matched_spp, type="tnrs_genbank")
    
    matches_without_replacements = copy.deepcopy(matched_spp)
    unmatched_without_replacements = copy.deepcopy(unmatched_input_spp)
    
    # 6. And now we try genus level matching to fill in a few remaining taxa
    unmatched_input_spp, unmatched_aln_spp, matched_spp = matches.genus_replacements(unmatched_input_spp, unmatched_aln_spp, matched_spp, type="clean_name")

    # Finally we print it all out.
    log.info("Here are your species matches, including generic level replacements: \n\n")
    for spp in matched_spp:    
        print spp, "\t", matched_spp[spp]
    
    for spp in unmatched_input_spp.values():
        print spp.original_name, "\t", "NA"
    
    print "\n\n\n"
    
    log.info("Here are your species matches, excluding generic level replacements: \n\n")
    for spp in matches_without_replacements:    
        print spp,"\t", matched_spp[spp]
    
    for spp in unmatched_without_replacements.values():
        print spp.original_name, "\t", "NA"
    