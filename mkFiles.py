
#  extract only backbone atoms and then store their coordinates

#file format
#0 	1   2    3      4    5      6               7          8        9         10            11
#ATOM	1   N   MET      A   1     -40.237         0.903     32.335    1.00       55.57         N  

#imports
import os
import ray as distri
#----------------------------------------------------------------------------------------
#This is for building the files with i=only required info
#It saves storage for parsing and enhances the speed of parsing
#reduces file size

from hitEnlist import  *

#----------------------------------------------------------------------------------------


distri.init()
@distri.remote
def  CoorFileMake(Acc):
    AccID=Acc
    fname=AccID + ".txt"
    inputF=open(fname)

    outFInit=AccID + ".ATOMS"
    out=open(outFInit,"w")

    output=AccID+".BackboneCoor"
    Coor=open(output,"w")

	#-----------------
    for line in inputF:
        if line.startswith('ATOM') or line.startswith('HETATM'):
            out.write(line )
		 
	#Filtered file with only structural data
	#------------------
    inputF.close()
    out.close()

    scan=open(outFInit)
	#------------------

    for line in scan:
        array=[]
        array=line.split()
        atom=array[2]
        row=array[3]+"    " +array[2]+ "    " + array[6]+ "     "+ array[7]+ "     "+ array[8]+"    " +array[5]
        Coor.write(row +"\n")
	 
	 #Final file with only backbone data in format aa3code  atom      x       y       z     numb       
	 
    scan.close()
    os.remove(fname)
    os.remove(outFInit)
	#Removing unecesarry Intermidiate files
#--------------------------------------------------------------------------------------------------------

res=[CoorFileMake.remote(Acc) for Acc in hits]
result=distri.get(res)
distri.shutdown()
exit()   

#-----------------------------------------------------------------------------------------------------------


