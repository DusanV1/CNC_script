import sys
import re

def CNN(argv):
    lines1=[]
    lines2=[]
    lines3=[]
    valuesX=[]
    valuesY=[]
    vrtaniPoradi={}

    # file1 = open("D327971_fc1.i", "r") 
    # print(argv[1])
    file1 = open(argv[1], "r") 
    lines1=file1.readlines()
    file1.close()
    vrtani=0

    for line in lines1:
        if re.findall("Zacatek bloku vrtani",line)!=[]:
            vrtani=1
            lines2.append(line)
            lines2.append("\n")
            
        elif re.findall("Konec bloku vrtani",line)!=[]:
            vrtani=2
        
        if vrtani==1:
            souradnice=re.findall("^X.[0-9]*[.,][0-9]*Y.[0-9]*[.,][0-9]*",line)
            if souradnice!=[]:
                souradniceX=re.findall("^X.[0-9]*[.,][0-9]*",souradnice[0])
                souradniceX=re.sub("X","",souradniceX[0])
                souradniceX=float(souradniceX)
                valuesX.append(souradniceX)
                # souradniceX=float(re.findall("[0-9]*[.,][0-9]*",souradniceX[0])[0])
                if souradniceX>50:
                    souradniceY=re.findall("Y.[0-9]*[.,][0-9]*$",souradnice[0])
                    souradniceY=re.sub("Y","",souradniceY[0])
                    souradniceY=float(souradniceY)
                    valuesY.append(souradniceY)
                    # souradniceY=float(re.sub("Y","",souradnice[0])[0])
                    # souradniceY=float(re.findall(".[0-9]*[.,][0-9]*$",souradnice[0])[0])
                    souradniceY10=souradniceY+10
                    lineNew=re.sub(str(souradniceY),str(souradniceY10),line) 
                    line=lineNew   
            # lines2.append(line)
                nastroj=re.findall("T[0-9]{2}$",line)
                if nastroj!=[]:
                    poradi=int(re.findall("[0-9]{2}",nastroj[0])[0])
                    vrtaniPoradi[poradi]=[]
                vrtaniPoradi[poradi].append(line)
        elif vrtani==0:
            lines2.append(line)
        elif vrtani==2:
            lines3.append(line)

    # print(vrtaniPoradi)   
            
    for i in range(len(vrtaniPoradi)):
        for k in range(len(vrtaniPoradi[i+1])):
            lines2.append(vrtaniPoradi[i+1][k])  
        
    for line in lines3:
        lines2.append(line)          
                    
    file2=open("cnc.txt","w")
    # file2.writelines(lines2)
    for line in lines2:
        file2.write(str(line))
    file2.close()            
                

    file3=open("souradniceExtreme.txt","w")
    file3.write("X_min/X_max/Y_min/Y_max\n")
    file3.write("{}/{}/{}/{}".format(min(valuesX),max(valuesX),min(valuesY),max(valuesY)))
    file3.close()    

if __name__ == "__main__":
    CNN(sys.argv)
# print(max(valuesX))    
            # # najit jestli tam je T0X
            # nastroj=re.findall("T[0-9]{2}$",line)
            # if nastroj!=[]:
            
            
        
        
        
    # with open("D327971_fc1.i") as f:
    #     lines=f.readlines
    
