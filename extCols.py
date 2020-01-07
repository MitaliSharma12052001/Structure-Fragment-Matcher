def extract_col(fn,col):
    column=[]
    f=open(fn)
    with  f:
        for line in f:
            chars=[]
            line=line.split("    ")
            for char in line:
                if char not in ['',' ']:
                    chars.append(char)
                    chars=' '.join(chars)
                    chars=chars.split()
                    if len(chars)>col:
                        column.append(chars[col])
    f.close()
    return column

    

 
