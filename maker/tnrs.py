import logging
log = logging.getLogger("tnrs")
import urllib2
import json

def tnrs_lookup(namelist):
    
    base_url = "http://tnrs.iplantc.org/tnrsm-svc/matchNames?retrieve=best&names="

    names=",".join(namelist)

    url = urllib2.quote("%s%s" %(base_url, names), safe="%/:=&?~#+!$,;'@()*[]")

    response = urllib2.urlopen(url).read()

    #extract a dictionary from the result
    try: 
        result = json.loads(unicode(response))['items']
        log.debug("Fetched tnrs result for list of %d species" % len(namelist))
    except:
        log.error("Couldn't get tnrs response for list of %d species" % len(namelist))
        result = [{'acceptedName': "NA"}]
            
    return result

def get_acceptednames(tnrs_dict):

    acceptednames = []
    
    for i in tnrs_dict:
        acceptedname = i['acceptedName']
    
        if acceptedname=="": acceptedname = "NA"
        
        acceptednames.append(acceptedname)
    
    return acceptednames
    
def check_one_species(name):
    
    r = tnrs_lookup([name])
    n = get_acceptednames(r)
        
    return n[0]

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
    
def check_many_species(namelist):
    
    chunksize = 500
    
    if len(namelist)<chunksize:
        r = tnrs_lookup(namelist)
        n = get_acceptednames(r)
    else:
        n = []
        for chunk in chunks(namelist, chunksize):        
            r = tnrs_lookup(chunk)
            if r != "NA":
                n = n + get_acceptednames(r)
            else:
                l = ["NA"]*chunksize
                n = n + l
            print n
    return n

def get_tnrs_dict(namelist):
    
    d = {}
    n = check_many_species(namelist)
    for i in range(len(namelist)):
        d[namelist[i]] = n[i]
    
    return d
    
    

if __name__ == "__main__":
    
    import random
    import string
    
    r = check_one_species("Zea mays")
    print r
    

    namelist = []
    
    for i in range(1005):
        genus = ''.join(random.choice(string.ascii_letters) for x in range(5))
        spp = ''.join(random.choice(string.ascii_letters) for x in range(5))
        namelist.append("%s %s" %(genus, spp))    
    
    n = check_many_species(namelist)
    for i in range(len(namelist)):
        print namelist[i], ",", n[i]