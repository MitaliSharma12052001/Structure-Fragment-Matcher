#make the array 
from hitEnlist import *
from converter import Converter
from extCols import *
import ray as distri
import os
#this module defines the functions for parsing the obtained data
#Z matrix is built from the cartesion cordinates
#bond length ang angles are whence obtained as lists



parsed=[]#list tuple of accID and data



@distri.remote
def makeZ(AccID):
    data={}#each hits data in dict
    Conv = Converter()
    Conv.run_cartesian(input_file=(AccID +".BackboneCoor"), output_file=(AccID+".zm"))
    data.__setitem__("len",extLength(AccID))
    data.__setitem__("ang",extAngle(AccID))
    aaAtomNum=extAAatomNum(AccID)
    data.__setitem__("aa",aaAtomNum[0])
    data.__setitem__("atom",aaAtomNum[1])
    data.__setitem__("num",aaAtomNum[2])
    listo=[AccID,data]
    os.remove(AccID+".BackboneCoor")
    os.remove(AccID+".zm")
    return listo

def extLength(Acc):
    leng=[]
    fn=Acc+".zm"
    leng=extract_col(fn,2)
    return leng
def extAngle(Acc):
    ang=[]
    fn=Acc+".zm"
    ang=extract_col(fn,4)
    return ang
def extAAatomNum(Acc):
    fn=Acc + ".zm"
    AA_atoms_num=(extract_col(fn,7),extract_col(fn,8),extract_col(fn,9))
    return AA_atoms_num
   

