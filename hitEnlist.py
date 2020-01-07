#enlist hits
from  extCols import  *
searchTxt=[]

for i in extract_col("hits.txt",1)[1:]:
    searchTxt.append(i[:4])
hits=[]
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
      
# Driver Code 
hits=Remove(searchTxt)
