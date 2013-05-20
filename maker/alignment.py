import os

import logging
log = logging.getLogger("species")


def write(alignment_spp, alnfile):
    
    log.info("Writing alignment for %d species" %len(alignment_spp))
    
    aln = open(alnfile, "r")
    sites = int(aln.readline().split()[1])
    spp = len(alignment_spp)
    header = "%d\t%d\n" %(spp, sites)

    outdir = os.path.dirname(alnfile)
    outfilename = os.path.join(alnfile, "treemaker_alignment.phy")

    outfile = open(outfilename, "w")
    outfile.write(header)
    
    for line in iter(aln):
        name = line.split()[0]
        if name in alignment_spp:
            outfile.write(line)
    
    log.info("Alignment is here: %s" % outfilename)