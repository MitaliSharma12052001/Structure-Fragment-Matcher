from hitEnlist import *
import ray as distrib
import requests
#this module is the slowest process
#makes multiple network calls 
#downloads pdb data for the hits

#---------------------------------------------------------

webL="https://files.rcsb.org/view/"



distrib.init()
@distrib.remote
def obtPDB(ihit):
    AccID=ihit
    url=webL + AccID + ".pdb"
    res = requests.get(url)

    res.raise_for_status()
    fname=AccID + ".txt"
    playFile = open(fname, 'wb')

    for chunk in res.iter_content(100000):
        playFile.write(chunk)
    return url



x=[obtPDB.remote(i) for i in hits]
y=distrib.get(x)
distrib.shutdown()
