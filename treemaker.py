

import sys
from maker import main

if __name__ == "__main__":
    # Well behaved unix programs exits with 0 on success...
    sppfile = "/Users/Rob/Dropbox/Current_work/Lasantha/treemaker_input/spplist.txt"
    alnfile = "/Users/Rob/Dropbox/Current_work/Lasantha/treemaker_input/big_plants.cn.phy"
    outgp = "Ginkgo_biloba"
    
    
    sys.exit(main.main(sppfile, alnfile, outgp))
