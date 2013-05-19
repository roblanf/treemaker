import logging
log = logging.getLogger("matches")


def exact(unmatched_input_spp, unmatched_aln_spp, matched_spp):
    """ look for exact matches between the keys of two dictionaries """
    
    log.info("Looking for exact matches between species dictionaries")
    log.debug("size of inputs: %d" %(len(unmatched_input_spp)))
    matches = set(unmatched_input_spp) & set(unmatched_aln_spp)

    unmatched_input_spp, unmatched_aln_spp, matched_spp = process_matches(unmatched_input_spp, unmatched_aln_spp, matched_spp, matches)
    
    log.info("%d exact matches found" %len(matches))
    log.debug("size of inputs: %d" %(len(unmatched_input_spp)))
    log.info(matches)    
    log.debug(matched_spp)
    
    return unmatched_input_spp, unmatched_aln_spp, matched_spp

def process_matches(unmatched_input_spp, unmatched_aln_spp, matched_spp, matches):
    """ matches is a list of keys of the two dictionaries"""

    for match in matches:
        input_original = unmatched_input_spp.pop(match).original_name
        alnmt_original = unmatched_aln_spp.pop(match).original_name
        matched_spp[input_original] = alnmt_original
    
    return unmatched_input_spp, unmatched_aln_spp, matched_spp
    
def choose_maxdata_alnmt_spp(list):
    data = -1
    best = None
    for s in list:
        if s.data >= data:
            best = s
    return best
    

def exact_binomial(unmatched_input_spp, unmatched_aln_spp, matched_spp, type):
    """ look for exact binomial matches between species in the two lists """
    
    log.info("Looking for exact matches between alignment binomial and %s binomial" % type)
    log.debug("size of inputs: %d" %(len(unmatched_input_spp)))

    # build a dictionaries keyed by binomials
    alnmt_binomials = {}
    for s in unmatched_aln_spp.values():
        l = alnmt_binomials.setdefault(s.original_binomial, [])
        l.append(s)
        alnmt_binomials[s.original_binomial] = l

    input_binomials = {}
    for s in unmatched_input_spp.values():
        if type == "original":    
            input_binomials[s.original_binomial] = s
        if type == "spellchecked": 
            input_binomials[s.binomial] = s
        if type == "original_genbank": 
            input_binomials[s.original_genbank_binomial] = s
        if type == "tnrs_genbank": 
            input_binomials[s.tnrs_genbank_binomial] = s

    matches = set(input_binomials) & set(alnmt_binomials)
    log.info("%d binomial matches found" %len(matches))
    log.info(matches)    
    
    for match in matches:
        input_s = input_binomials[match]
        input_original = input_s.original_name
        unmatched_input_spp.pop(input_s.clean_name)
        
        alnmt_s = choose_maxdata_alnmt_spp(alnmt_binomials[match])        
        alnmt_original = alnmt_s.original_name
        unmatched_aln_spp.pop(alnmt_s.clean_name)
        matched_spp[input_original] = alnmt_original

    log.debug("size of inputs: %d" %(len(unmatched_input_spp)))
    log.debug(matched_spp)
    
    return unmatched_input_spp, unmatched_aln_spp, matched_spp
     
  
def spellchecked_binomial(unmatched_input_spp, unmatched_aln_spp, matched_spp):
    """ look for exact binomial matches between species in the two lists """
    
    log.info("Looking for matches when translating inputs to tnrs accepted binomials")
    log.debug("size of inputs: %d" %(len(unmatched_input_spp)))

    # build a dictionaries keyed by binomials
    alnmt_binomials = {}
    for s in unmatched_aln_spp.values():
        l = alnmt_binomials.setdefault(s.original_binomial, [])
        l.append(s)
        alnmt_binomials[s.original_binomial] = l

    input_binomials = {}
    for s in unmatched_input_spp.values():
        input_binomials[s.binomial] = s

    matches = set(input_binomials) & set(alnmt_binomials)
    log.info("%d spellchecked binomial matches found" %len(matches))
    log.info(matches)    
    
    for match in matches:
        input_s = input_binomials[match]
        input_original = input_s.original_name
        unmatched_input_spp.pop(input_s.clean_name)
        
        alnmt_s = choose_maxdata_alnmt_spp(alnmt_binomials[match])        
        alnmt_original = alnmt_s.original_name
        unmatched_aln_spp.pop(alnmt_s.clean_name)
        matched_spp[input_original] = alnmt_original

    log.debug("size of inputs: %d" %(len(unmatched_input_spp)))
    log.debug(matched_spp)
    
    return unmatched_input_spp, unmatched_aln_spp, matched_spp
  
  
  
    