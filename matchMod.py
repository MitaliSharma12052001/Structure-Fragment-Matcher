from __future__ import division
from hitEnlist import *
from parse import *
import ray as distri
# matching module


q=[]#query protein
distri.init(ignore_reinit_error=True)
x=[makeZ.remote(i) for i in hits]
parsed=distri.get(x)
scoreArr=[]
@distri.remote
def matchIt(db, q , ident):
    angSc=matchAng(db,q)
    lenSc=matchLen(db,q)
    Score=[]
    Score=[angSc,lenSc]
    sc=0.75*angSc+0.25*lenSc#Appxmn
    res=(ident,sc)
    return res
    

def matchAng(d,q):
    cum=0
    for i in range(min(len(d["ang"]),len(q[1]))):
        diff=abs(float(q[1][i])-float(d["ang"][i]))*100/359
        anDiff=100-diff
        cum+=anDiff
    sc=cum/len(q)
    return sc
def matchLen(d,q):
    cum=0
    for i in range(min(len(d["len"]),len(q[0]))):
        if not( float(q[0][i])==0 or float(d["len"][i])==0 ):
            if float(q[0][i])>=float(d["len"][i]):
                rat=float(d["len"][i])//float(q[0][i])*100
            else:
                rat=float(q[0][i])//float(d["len"][i])*100
    return rat
idd,qd=parsed[0]
q.append(qd["len"])
q.append(qd["ang"])
x=[matchIt.remote(db[1],q,db[0]) for db in parsed]
scoreArr=distri.get(x)
print(scoreArr)
distri.shutdown()
