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

def mesh_ports(a,dim,prefix1,prefix2):
    r = range(1,dim+1)
    line = ""
    for y in r:
        for x in r:   
            line+= prefix1 + str(x + (y-1)*dim) + ","
    a(line)
    line_l = ""
    line_r = ""
    line_t = ""
    line_b = ""
    for y in r:
        for x in r:
            if(x==1):   
                line_l+= prefix2+  "XL" + str(x + (y-1)*dim) + ","
            if(x==dim):
                line_r+= prefix2+ "XR" + str(x + (y-1)*dim) + ","
            if(y==1):
                line_t+= prefix2+ "YT" + str(x + (y-1)*dim) + ","
            if(y==dim):
                line_b+= prefix2+ "YB" + str(x + (y-1)*dim) + ","
    a(line_l)
    a(line_r)
    a(line_b)
    a(line_t)

def mesh_channels(a,dim,prefix1,prefix2):
    r = range(1,dim+1)
    for y in r:
        for x in r:
            myid = str(x + (y-1)*dim) 
            if(x==1):   
               a("{" + prefix2+ "XL" + myid+ ", R" + myid+'.'+ prefix2 +"XL}")
            if(x==dim):
                a("{" + prefix2+ "XR" + myid+ ", R" + myid+'.' +prefix2 +"XR}")
            if(y==1):
                a("{"  +prefix2+ "YT" + myid+ ", R" + myid+ '.'+prefix2 +"YT}")
            if(y==dim):
                a("{"  +prefix2+ "YB" + myid+ ", R" + myid+ '.'+prefix2 +"YB}")
           


def cook_mesh(dim,dest):
   
    lines = []
    r = range(1,dim+1)
    a = lambda line:lines.append(line + "\n")
    a('import "Router.poosl"')
    a('cluster class Meshnxn (FifoCapacity: Integer, FifoProcessingTime: Real, RouterProcessingTime: Real)')  
    a('ports')
    mesh_ports(a,dim,"In","I")
    mesh_ports(a,dim,"Out","O")
    lines[-1] = lines[-1][:-2]+"\n"
    a('')
    a('instances')
    r2 = range(1,dim)
    
    baseline = ": Fifo(Capacity := FifoCapacity, ProcessingTime := FifoProcessingTime)"
    for y in r:
        for x in r:
            if(x<dim):   
                a("F" + str(x + (y-1)*dim) + str(x + 1  + (y-1)*dim) + baseline) 
            if(x>1):
                a("F" + str(x +  (y-1)*dim) + str(x -1 + (y-1)*dim) + baseline) 
            if(y<dim):
                a("F" + str(x + (y-1)*dim) + str(x + y*dim) + baseline) 
            if(y>1):
                a("F" + str(x + (y-1)*dim) + str(x + (y-2)*dim) + baseline) 
    for y in r:
        for x in r:
            myid = str(x + (y-1) * dim)
            a("R" + myid +": Router(FifoCapacity := FifoCapacity, FifoProcessingTime := FifoProcessingTime, RouterProcessingTime := RouterProcessingTime)")
    
    a('channels')
    for y in r:
        for x in r:
            myid = str(x + (y-1) * dim)
            a('{In'+myid+ ', R'+myid+'.In }')
            a('{Out'+myid+ ', R'+myid+'.Out }')
    mesh_channels(a,dim,"In","I")
    mesh_channels(a,dim,"Out","O")
    
    for y in r:
        for x in r:
            if(x<dim):
                id1=  str(x + (y-1)*dim)
                id2 =str(x + 1  + (y-1)*dim) 
                myf = "F" + id1  + id2 
                a('{' +myf+ ".In"+ ', ' + "R" + id1 + ".OXR" + '}')
                a('{' +myf+ ".Out"+ ', ' + "R" + id2 + ".IXL" +'}')
            if(x>1):
                id1=  str(x  +(y-1)*dim)
                id2 =str(x - 1  + (y-1)*dim) 
                myf = "F" + id1  + id2 
                a('{' +myf+ ".In"+ ', ' + "R" + id1 + ".OXL" + '}')
                a('{' +myf+ ".Out"+ ', ' + "R" + id2 + ".IXR" +'}')
            if(y<dim):
                id1=  str(x + (y-1)*dim)
                id2 = str(x  + (y)*dim) 
                myf = "F" + id1  + id2 
                a('{' +myf+ ".In"+ ', ' + "R" + id1 + ".OYB" + '}')
                a('{' +myf+ ".Out"+ ', ' + "R" + id2 + ".IYT" +'}') 
            if(y>1):
                id1=  str(x + (y-1)*dim)
                id2 = str(x  + (y-2)*dim) 
                myf = "F" + id1  + id2 
                a('{' +myf+ ".In"+ ', ' + "R" + id1 + ".OYT" + '}')
                a('{' +myf+ ".Out"+ ', ' + "R" + id2 + ".IYB" +'}')  



    f = open(dest,'w')
    f.writelines(lines)
    f.close()           

#cook_copypasta('BasedNetworkSource.poosl','output.poosl',10)



