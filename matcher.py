from __future__ import division
from hitEnlist import *
from parse import *
import ray as distri
from pprint import pprint



# matching module


q=[]#query protein
distri.init(ignore_reinit_error=True)
x=[makeZ.remote(i) for i in hits]
parsed=distri.get(x)
scoreArr=[]
 
  
# Function to sort hte list by second item of tuple 
def Sort_Tuple(tup,o):  
  
    # reverse = None (Sorts in Ascending order)  
    # key is set to sort using o+1th element of  
    # sublist lambda has been used  
    tup.sort(key = lambda x: x[o])  
    return tup  

selPts=[219,237,249,372,373]#list of pts

@distri.remote
def matchIt(db, q ,ident,selPts):
    scoreTotal=0
    scList=matchAng_Len(db,q,selPts)
    atomList=[]
    for j in range(len(selPts)):
        scoreTotal+=scList[j][2]
        k=int(scList[j][1])
        loc=(db["aa"][k],db["atom"][k],db["num"][k])
        queryLoc=(q[2][0][selPts[j]],q[2][1][selPts[j]],q[2][2][selPts[j]])
        atomList.append((queryLoc,loc))
    perc=scoreTotal/maxSc *100
    res=(ident,perc, atomList)
    return res

#--------------------------------------

    


def matchAng_Len(d,q,selectedPts):
    iScores=[] #keeps the scores in the format of maxMatch
    Count=len(selectedPts)
    maxMatch=[]
    for ii in range(Count):
        maxMatch.append((0,0,0))#keeps the scores in the format =(SelectedItem_query,PosnOfMatch'sCoor,score),with only unique ij pairs are entered acc to score

    for i in selectedPts:
        listSc=[]#for each i takes top m entries , where m>=4 is the num of atoms selected from query
        for j in range(len(d["aa"])):
            diff=abs(float(q[1][i])-float(d["ang"][j]))*100/359 #difference between torsion angles
            anDiff=100-diff
            if not( float(q[0][i])==0 or float(d["len"][j])==0 ):
                if float(q[0][i])>=float(d["len"][j]):
                    rat=float(d["len"][j])//float(q[0][i])*100
                else:
                    rat=float(q[0][i])//float(d["len"][j])*100
            else:
                rat=100##ratio of lengths
            sc=0.75*anDiff+0.25*rat#Appxmn formula of contribution
            listSc.append((j,sc))
        listSc=Sort_Tuple(listSc,1)#sorting list acc to scores
        listSc=listSc[:Count]#taking top m scores only
        for mm in listSc:
            iScores.append((i,mm[0],mm[1]))
    iScores=Sort_Tuple(iScores,2)
    DoneJ=[]
    DoneI=[]
    for AtomBeingMatched in range(Count):
        ind=0
        while maxMatch[AtomBeingMatched]==(0,0,0):
            if iScores[ind][1] in DoneJ or iScores[ind][0] in DoneI:
                ind=ind+1
            else:
                maxMatch[AtomBeingMatched]=iScores[ind]
                DoneJ.append(iScores[ind][1])
                DoneI.append(iScores[ind][0])
    
    return maxMatch


idd,qd=parsed[0]
q.append(qd["len"])
q.append(qd["ang"])
ident=(qd["aa"],qd["atom"],qd["num"])
q.append(ident)


def MaxFind(d,q,selPts):
    scoreTotal=0
    scList=matchAng_Len(d,q,selPts)
    for j in range(len(selPts)):
        scoreTotal+=scList[j][2]
    return scoreTotal


maxSc=MaxFind(parsed[0][1],q,selPts)

x=[matchIt.remote(db[1],q,db[0],selPts) for db in parsed]
scoreArr=distri.get(x)
pprint(scoreArr)
distri.shutdown()
