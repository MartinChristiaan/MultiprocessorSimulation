# Read file
# for lines strip every character that is a number
# duplicates?



def cook_copypasta(source,dest,nduplicates):
    f = open(source,'r')
    lines = f.readlines()
    lines_nonumbers = [''.join([i for i in line if not i.isdigit()]).strip() for line in lines]
    lines_numberpositions = [[id for id in range(len(line)) if line[id].isdigit()] for line in lines]
    i = 0
    while i < len(lines_nonumbers)-1:
        duplicating = False
        while i+1 < len(lines_nonumbers) and lines_nonumbers[i] == lines_nonumbers[i+1]:
            del lines_nonumbers[i+1]
            del lines[i+1]
            del lines_numberpositions[i+1]
            duplicating = True
        if duplicating:
            for j in range(nduplicates-1):
                #print(str(len(lines)) + " , ins : " + str(i+j+1))
                myline = lines[i]
                pos_shift=0
                for num_pos in lines_numberpositions[i]:
                    myline = myline[:num_pos+pos_shift] + str(j+2) + myline[num_pos+1+pos_shift:]
                    pos_shift+=len(str(j+2))-1

                lines.insert(i+j+1,myline)
                lines_numberpositions.insert(i+j+1,[])
                lines_nonumbers.insert(i+j+1,"")
            
            i+=nduplicates
        if i < len(lines):
            words = lines[i].split()
            #wordswnumbers = [word for word in words if len(''.join([i for i in word if i.isdigit()])) > 0]
            words_stripped = [''.join([i for i in word if not i.isdigit()]).strip() for word in words]

            words_numberpositions = [[id for id in range(len(word)) if word[id].isdigit()] for word in words]
            k = 0
        

            while k < len(words_stripped)-1:
                
                duplicating = False
                contains_digit = len(''.join([i for i in words[k] if i.isdigit()])) > 0 
                while contains_digit and k < len(words_stripped)-1 and words_stripped[k].replace(',','') == words_stripped[k+1].replace(',',''):
                    del words_stripped[k+1]
                    del words[k+1]
                    del words_numberpositions[k+1]
                    duplicating = True
                if duplicating:
                    for j in range(nduplicates-1):
                        myword = words[k]
                        for num_pos in words_numberpositions[k]:
                            myword = myword[:num_pos] + str(j+2) + myword[num_pos+1:]
                            if j == nduplicates-2 and myword[-1] == ',':
                               myword = myword[:-1]     
                        words.insert(k+j+1,myword)
                        words_numberpositions.insert(k+j+1,[])
                        words_stripped.insert(k+j+1,"")                
                    
                    k+=nduplicates
                k+=1
            lines[i] = ' '.join(words) + '\n'

        # words with numbers
        # 
        # split line no number
        # duplicates?
        # Remove duplicates
        # if word contains number
        
        i+=1        
    f = open(dest,'w')
    f.writelines(lines)
    f.close()

def mesh_ports(a,dimx,dimy,prefix1,prefix2):
    rx = range(1,dimx+1)
    ry = range(1,dimy+1)
    line = ""
    for y in ry:
        for x in rx:   
            line+= prefix1 + str(x + (y-1)*dimx) + ","
    a(line)
    line_l = ""
    line_r = ""
    line_t = ""
    line_b = ""
    for y in ry:
        for x in rx:
            if(x==1):   
               line_l+= prefix2+  "XL" + str(x + (y-1)*dimx) + ","
            if(x==dimx):
                line_r+= prefix2+ "XR" + str(x + (y-1)*dimx) + ","
            if(y==1):
                line_t+= prefix2+ "YT" + str(x + (y-1)*dimx) + ","
            if(y==dimy):
                line_b+= prefix2+ "YB" + str(x + (y-1)*dimx) + ","
    a(line_l)
    a(line_r)
    a(line_b)
    a(line_t)

def mesh_channels(a,dimx,dimy,prefix1,prefix2):
    rx = range(1,dimx+1)
    ry = range(1,dimy+1)
    for y in ry:
        for x in rx:
            myid = str(x + (y-1)*dimx) 
            if(x==1):   
               a("{" + prefix2+ "XL" + myid+ ", R" + myid+'.'+ prefix2 +"XL}")
            if(x==dimx):
                a("{" + prefix2+ "XR" + myid+ ", R" + myid+'.' +prefix2 +"XR}")
            if(y==1):
                a("{"  +prefix2+ "YT" + myid+ ", R" + myid+ '.'+prefix2 +"YT}")
            if(y==dimy):
                a("{"  +prefix2+ "YB" + myid+ ", R" + myid+ '.'+prefix2 +"YB}")

def cook_mesh(dimx,dimy,dest):
   
    lines = []
    rx = range(1,dimx+1)
    ry = range(1,dimy+1)
    a = lambda line:lines.append(line + "\n")
    a('import "Router.poosl"')
    a('cluster class Meshnxn (FifoCapacity: Integer, FifoProcessingTime: Real, RouterProcessingTime: Real)')  
    a('ports')
    mesh_ports(a,dimx,dimy,"In","I")
    mesh_ports(a,dimx,dimy,"Out","O")
    lines[-1] = lines[-1][:-2]+"\n"
    a('')
    a('instances')
    
    baseline = ": Fifo(Capacity := FifoCapacity, ProcessingTime := FifoProcessingTime)"
    for y in ry:
        for x in rx:
            if(x<dimx):   
                a("F" + str(x + (y-1)*dimx) + str(x + 1  + (y-1)*dimx) + baseline) 
            if(x>1):
                a("F" + str(x +  (y-1)*dimx) + str(x -1 + (y-1)*dimx) + baseline) 
            if(y<dimy):
                a("F" + str(x + (y-1)*dimx) + str(x + y*dimx) + baseline) 
            if(y>1):
                a("F" + str(x + (y-1)*dimx) + str(x + (y-2)*dimx) + baseline) 
    for y in ry:
        for x in rx:
            myid = str(x + (y-1) * dimx)
            a("R" + myid +": Router(FifoCapacity := FifoCapacity, FifoProcessingTime := FifoProcessingTime, RouterProcessingTime := RouterProcessingTime)")
    
    a('channels')
    for y in ry:
        for x in rx:
            myid = str(x + (y-1) * dimx)
            a('{In'+myid+ ', R'+myid+'.In }')
            a('{Out'+myid+ ', R'+myid+'.Out }')

    mesh_channels(a,dimx,dimy,"In","I")
    mesh_channels(a,dimx,dimy,"Out","O")
    
    for y in ry:
        for x in rx:
            if(x<dimx):
                id1=  str(x + (y-1)*dimx)
                id2 =str(x + 1  + (y-1)*dimx) 
                myf = "F" + id1  + id2 
                a('{' +myf+ ".In"+ ', ' + "R" + id1 + ".OXR" + '}')
                a('{' +myf+ ".Out"+ ', ' + "R" + id2 + ".IXL" +'}')
            if(x>1):
                id1=  str(x  +(y-1)*dimx)
                id2 =str(x - 1  + (y-1)*dimx) 
                myf = "F" + id1  + id2 
                a('{' +myf+ ".In"+ ', ' + "R" + id1 + ".OXL" + '}')
                a('{' +myf+ ".Out"+ ', ' + "R" + id2 + ".IXR" +'}')
            if(y<dimy):
                id1=  str(x + (y-1)*dimx)
                id2 = str(x  + (y)*dimx) 
                myf = "F" + id1  + id2 
                a('{' +myf+ ".In"+ ', ' + "R" + id1 + ".OYB" + '}')
                a('{' +myf+ ".Out"+ ', ' + "R" + id2 + ".IYT" +'}') 
            if(y>1):
                id1=  str(x + (y-1)*dimx)
                id2 = str(x  + (y-2)*dimx) 
                myf = "F" + id1  + id2 
                a('{' +myf+ ".In"+ ', ' + "R" + id1 + ".OYT" + '}')
                a('{' +myf+ ".Out"+ ', ' + "R" + id2 + ".IYB" +'}')  



    f = open(dest,'w')
    f.writelines(lines)
    f.close()           


def cook_torus(dimx,dimy,dest):
   
    lines = []
    a = lambda line:lines.append(line + "\n")
    a('import "Router.poosl"')
    a('import "TDMFifo.poosl"')
    a('cluster class Torusnxn (FifoCapacity: Integer, FifoProcessingTime: Real, RouterProcessingTime: Real)')  
    a('ports')
    rx = range(1,dimx+1)
    ry = range(1,dimy+1)
    
    def mid(x,y):
        return str(x + (y-1)*dimx)

    line = ""
    for y in ry:
        for x in rx:   
            line+= "In" + mid(x,y) + ","
    a(line)
    line = ""
    for y in ry:
        for x in rx:   
            line+= "Out" + mid(x,y) + ","
    a(line)
    
    ## Disconnected ports
    for x in rx:
        for y in ry:
            if x == 1:
                a('IXL1_' + mid(x,y)+ ",")
            if y == 1:
                a('IYT1_' + mid(x,y)+ ",")
            if x >= dimx-1:
                a('OXR2_' + mid(x,y)+ ",")
            if y >= dimy-1:
                a('OYB2_' + mid(x,y)+ ",")
            if x == dimx : 
                a('IXL2_' + mid(x,y)+ ",")
            if y == dimy : 
                a('IYT2_' + mid(x,y)+ ",")
                
                
    lines[-1] = lines[-1][:-2]+"\n" # remove comma

    a('')
    a('instances')
    
    baseline1 = ": Fifo(Capacity := FifoCapacity, ProcessingTime := FifoProcessingTime)"
    baseline2 = ": TDMFifo(Capacity := FifoCapacity, ProcessingTime := FifoProcessingTime)"
    
    for y in ry:
        for x in rx:
            right = mid(x+1,y)
            if x == dimx:
                right = mid(1,y)
            if x < dimx-1:
                a("F" + mid(x,y) + right + baseline2)
            else:
                a("F" + mid(x,y) + right + baseline1)

            down = mid(x,y+1)
            if y == dimy:
                down = mid(x,1)
            if y < dimy-1:
                a("F" + mid(x,y) + down + baseline2)
            else:
                a("F" + mid(x,y) + down + baseline1)
             
    for y in ry:
        for x in rx:
            myid = str(x + (y-1) * dimx)
            a("R" + myid +": Router(RouterProcessingTime:= RouterProcessingTime,FifoCapacity := FifoCapacity,FifoProcessingTime := FifoProcessingTime,Xpos := "+ str(x) + ",Ypos := "+str(y)+",NumberOfXNodes:= "+str(dimx)+",NumberOfYNodes:= "+str(dimy)+")")
    
    a('channels')
    for y in ry:
        for x in rx:
            myid = str(x + (y-1) * dimx)
            a('{In'+myid+ ', R'+myid+'.In }')
            a('{Out'+myid+ ', R'+myid+'.Out }')    
    
    for y in ry:
        for x in rx:
            right = mid(x+1,y)

            if x < dimx-1:
                a("{F" + mid(x,y) + right + ".In1, R" + mid(x,y) + ".OXR1}" )
                a("{F" + mid(x,y) + right + ".In2, R" + mid(x,y) + ".OXR2}" )
                a("{F" + mid(x,y) + right + ".Out1, R" + right + ".IXL1}" )
                a("{F" + mid(x,y) + right + ".Out2, R" + right + ".IXL2}" )
            elif x == dimx:
                right = mid(1,y)
                a("{F" + mid(x,y) + right + ".In, R" + mid(x,y) + ".OXR1}" )
                a("{F" + mid(x,y) + right + ".Out, R" + right + ".IXL2}" )
            else:
                a("{F" + mid(x,y) + right + ".In, R" + mid(x,y) + ".OXR1}" )
                a("{F" + mid(x,y) + right + ".Out, R" + right + ".IXL1}" )

            down = mid(x,y+1)
            if y < dimy-1:
                a("{F" + mid(x,y) + down + ".In1, R" + mid(x,y) + ".OYB1}" )
                a("{F" + mid(x,y) + down + ".In2, R" + mid(x,y) + ".OYB2}" )
                a("{F" + mid(x,y) + down + ".Out1, R" + down + ".IYT1}" )
                a("{F" + mid(x,y) + down + ".Out2, R" + down + ".IYT2}" )
            elif y == dimy:
                down = mid(x,1)
                a("{F" + mid(x,y) + down + ".In, R" + mid(x,y) + ".OYB1}" )
                a("{F" + mid(x,y) + down + ".Out, R" + down + ".IYT2}" )
            else:
                a("{F" + mid(x,y) + down + ".In, R" + mid(x,y) + ".OYB1}" )
                a("{F" + mid(x,y) + down + ".Out, R" + down + ".IYT1}" )
    
    # Disconnected ports
    for x in rx:
        for y in ry:
            if x == 1:
                a('{IXL1_' + mid(x,y)+ ",R" + mid(x,y) + ".IXL1}")
            if y == 1:
                a('{IYT1_' + mid(x,y)+ ",R" + mid(x,y) + ".IYT1}")
            if x >= dimx-1:
                a('{OXR2_' + mid(x,y)+ ",R" + mid(x,y) + ".OXR2}")
            if y >= dimy-1:
                a('{OYB2_' + mid(x,y)+ ",R" + mid(x,y) + ".OYB2}")
            if x == dimx : 
                a('{IXL2_' + mid(x,y)+ ",R" + mid(x,y) + ".IXL2}")
            if y == dimy : 
                a('{IYT2_' + mid(x,y)+ ",R" + mid(x,y) + ".IYT2}")
 


    f = open(dest,'w')
    f.writelines(lines)
    f.close()           

def get_ids(x, y,dimx ,dimy):
    my_id = str(x + (y-1)*dimx)
    right = str(x+1 + (y-1)*dimx)
    if x == dimx:
        right = str(1+(y-1)*dimx) + "x"
    up = str(x + y*dimx)
    if y == dimy:
        up = str(x) + "x"
    left = str(x-1 + (y-1)*dimx)
    if x == 1:
        left = str(dimx + (y-1)*dimx) + "x"
    down = str(x + (y-2)*dimx)
    if y == 1:
        down = str(x + (dimy-1) * dimx)+ "x"
    return my_id, right, left, up, down


#cook_mesh(3,2,'output.poosl')
#cook_copypasta('BasedNetworkSource.poosl','output.poosl',10)

def cook_ring(dim,dest):
   
    lines = []
    a = lambda line:lines.append(line + "\n")
    a('import "Router.poosl"')
    a('import "TDMRouter.poosl"')
    a('import "TDMFifo.poosl"')
    a('cluster class Ringnxn (FifoCapacity: Integer, FifoProcessingTime: Real, RouterProcessingTime: Real)')  
    a('ports')
    r = range(1,dim+1)

    
    line = ""
    for x in r:   
       line+= "In" + str(x) + ","
    a(line)
    line = ""
    for x in r:   
        line+= "Out" + str(x) + ","
    a(line)
    a('IXL1_start,')
    a('OXR2_stop')

    a('')
    a('instances')
    
    baseline1 = ": Fifo(Capacity := FifoCapacity, ProcessingTime := FifoProcessingTime)"
    baseline2 = ": TDMFifo(Capacity := FifoCapacity, ProcessingTime := FifoProcessingTime)"
    
    for x in r:
        my_id = str(x)
        right = str(x+1)
        if x == dim:
            right = str(1)
        if x < dim - 1 :   
            a("F" + my_id + right + baseline2)
        else:
            a("F" + my_id + right + baseline1)
    for x in r:
        myid = str(x)
        if x == dim:
            a("R" + myid +": Router (ProcessingTime:= RouterProcessingTime,Xpos := "+ str(x)+ ",NumberOfXNodes:= "+str(dim)+")")
        else:
            a("R" + myid +": TDMRouter (ProcessingTime:= RouterProcessingTime,Xpos := "+ str(x)+ ",NumberOfXNodes:= "+str(dim)+")")
    
    a('channels')
    for x in r:
        myid = str(x)
        a('{In'+myid+ ', R'+myid+'.In }')
        a('{Out'+myid+ ', R'+myid+'.Out }')    
    
    for x in r:
        my_id = str(x)
        right = str(x+1)
        if x == dim:
            right = str(1)

        if x == 1:
            a("{IXL1_start,R" + str(x) + ".IXL1}")

        if x < dim - 1 :   
            a("{F" + my_id + right + ".In1, R"+my_id + ".OXR1" + "}")
            a("{F" + my_id + right + ".In2, R"+my_id + ".OXR2" + "}")
            a("{F" + my_id + right + ".Out1, R"+right + ".IXL1" + "}")
            a("{F" + my_id + right + ".Out2, R"+right + ".IXL2" + "}")
        elif x == dim-1:
            a("{F" + my_id + right + ".In, R"+my_id + ".OXR1" + "}")
            a("{F" + my_id + right + ".Out, R"+right + ".IXL1" + "}")
            a("{OXR2_stop,R" +str(x) + ".OXR2}")
        elif x == dim:
            a("{F" + my_id + right + ".In, R"+my_id + ".OXR1" + "}")
            a("{F" + my_id + right + ".Out, R"+right + ".IXL2" + "}")
    

    f = open(dest,'w')
    f.writelines(lines)
    f.close()           
