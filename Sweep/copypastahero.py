# Read file
# for lines strip every character that is a number
# duplicates?



def cook_copypasta(source,nduplicates):
    f = open(source,'r')
    lines = f.readlines()
    lines_nonumbers = [''.join([i for i in line if not i.isdigit()]).strip() for line in lines]
    lines_numberpositions = [[id for id in range(len(line)) if line[id].isdigit()] for line in lines]
    i = 0
    while i < len(lines_nonumbers)-1:
        duplicating = False
        while lines_nonumbers[i] == lines_nonumbers[i+1]:
            del lines_nonumbers[i+1]
            del lines[i+1]
            del lines_numberpositions[i+1]
            duplicating = True
        if duplicating:
            for j in range(nduplicates-1):
                #print(str(len(lines)) + " , ins : " + str(i+j+1))
                myline = lines[i]
                for num_pos in lines_numberpositions[i]:
                    myline = myline[:num_pos] + str(j+2) + myline[num_pos+1:]
                lines.insert(i+j+1,myline)
                lines_numberpositions.insert(i+j+1,[])
                lines_nonumbers.insert(i+j+1,"")
            
            i+=nduplicates
        i+=1        
    f = open("output.poosl",'w')
    f.writelines(lines)
cook_copypasta('BasedNetworkSource.poosl',3)



