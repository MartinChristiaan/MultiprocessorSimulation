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
        while lines_nonumbers[i] == lines_nonumbers[i+1]:
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
cook_copypasta('BasedNetworkSource.poosl','output.poosl',10)



