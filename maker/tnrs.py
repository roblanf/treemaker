import logging
logging.basicConfig(level="INFO")

import urllib2
import json

def check_one_species(binomial):
    
    base_url = "http://tnrs.iplantc.org/tnrsm-svc/matchNames?retrieve=best&names="
    url = urllib2.quote("%s%s" %(base_url, binomial), safe="%/:=&?~#+!$,;'@()*[]")
    response = urllib2.urlopen(url).read()

    logging.info(url)

    #extract a dictionary from the result
    try: 
        result = json.loads(unicode(response))['items'][0]
    except:
        logging.error("Couldn't get tnrs response for '%s'" % binomial)
        result = "NA"
        
    logging.info("Fetched tnrs result for '%s'" % binomial)
    
    return result
    
def get_acceptedname(tnrs_dict):
    acceptedname = tnrs_dict['acceptedName']
    
    if acceptedname=="": acceptedname = "NA"
    
    return acceptedname
    
if __name__ == "__main__":
    
    r = check_one_species("Zea mays")
    print r
    
    s = get_acceptedname(r)
    print s