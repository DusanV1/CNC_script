 
import sys
import re
 
def CNC(fileName,extremeVal=0):
    lines1=[]
    lines2=[]
    lines3=[]
    valuesX=[]
    valuesY=[]
    vrtaniPoradi={}
 
    # open and read file for CNC
    file1 = open(fileName, "r")
    lines1=file1.readlines()
    file1.close()
    vrtani=0
 
    for line in lines1:
        # Define part for drilling and modification
        if re.findall("Zacatek bloku vrtani",line)!=[]:
            vrtani=1
            lines2.append(line)
            lines2.append("\n")          
        elif re.findall("Konec bloku vrtani",line)!=[]:
            vrtani=2
            lines3.append("\n")
            lines3.append("$\n")
            lines3.append("\n")
       
        if vrtani==1:
            souradnice=re.findall("^X.[0-9]*[.,][0-9]*Y.[0-9]*[.,][0-9]*",line)
            if souradnice!=[]:
                # select X direction and choce the one above 50
                souradniceX=re.findall("^X.[0-9]*[.,][0-9]*",souradnice[0])
                souradniceX=re.sub("X","",souradniceX[0])
                souradniceX=float(souradniceX)
                valuesX.append(souradniceX)
                # valuesX.append(souradniceX)
               
                # Select Y direction and add 10 to one where X>50
                souradniceY=re.findall("Y.[0-9]*[.,][0-9]*$",souradnice[0])
                souradniceY=re.sub("Y","",souradniceY[0])
                souradniceY=float(souradniceY)
                valuesY.append(souradniceY)
                if souradniceX>50:
                    souradniceY10=souradniceY+10
                    lineNew=re.sub(str(souradniceY),str(souradniceY10),line)
                    line=lineNew  
                   
                # Choose line with tool definition T0X
                nastroj=re.findall("T[0-9]{2}$",line)
                if nastroj!=[]:
                    poradi=int(re.findall("[0-9]{2}",nastroj[0])[0])
                    vrtaniPoradi[poradi]=[]
                # populate dictionary with blocks for each tool type
                vrtaniPoradi[poradi].append(line)
        elif vrtani==0:
            lines2.append(line)
        elif vrtani==2:
            lines3.append(line)
   
    # Put all parts of a text together        
    for i in range(len(vrtaniPoradi)):
        for k in range(len(vrtaniPoradi[i+1])):
            lines2.append(vrtaniPoradi[i+1][k])  
       
    for line in lines3:
        lines2.append(line)          
   
    if extremeVal==0:
        # Create file with sorted coordinates based on the tool type and Y+10 for X>50                
        file2=open("cnc.txt","w")
        for line in lines2:
            file2.write(str(line))
        file2.close()  
    else:  
        return valuesX, valuesY            
                 
   
def extremeCoords(fileName):
    # lines1=[]
    valuesX=[]
    valuesY=[]
 
    valuesX, valuesY=CNC(fileName,1)          
               
    # Created file with min and max of X and Y coordinates
    file3=open("souradniceExtreme.txt","w")
    file3.write("X_min/X_max/Y_min/Y_max\n")
    file3.write("{}/{}/{}/{}".format(min(valuesX),max(valuesX),min(valuesY),max(valuesY)))
    file3.close()  
 
if __name__ == "__main__":
    globals()[sys.argv[1]](sys.argv[2])
    # CNC(sys.argv)
 
 
 