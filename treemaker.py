

import sys
from maker import main

if __name__ == "__main__":
    # Well behaved unix programs exits with 0 on success...
    sppfile = "/Users/Rob/Documents/Projects_Current/treemaker/example/spplist.txt"
    alnfile = "/Users/Rob/Documents/Projects_Current/treemaker/example/test.phy"
    match_genera = False
    
    
    sys.exit(main.main(sppfile, alnfile, match_genera))
