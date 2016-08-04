#!/usr/bin/python


def lld_render(itemList,itLab):
    '''renders in a LLD suitable format  
    a list of items, using the given list of labels
    It preliminary checks if dimensions are correct  
    '''


    if len(itemList[0]) != len(itLab):
        print "FATAL : item and label lists have different dimensions"
        return -1

    preamble="{\"data\":[\n"
    postamble="\n]}"
    body=""

    for el in itemList:
       # body+="{\"{#%s}\":\"%s\",\"{#%s}\":\"%s\",\"{#%s}\":\"%s\",\
#"{#%s}\":\"%s\",\"{#%s}\":\"%s\"},\n"\
 #       #        %(itLab[0],el[0],itLab[1],el[1],itLab[2],el[2],itLab[3],el[3],itLab[4],el[4])
         bodyPre="{"
         bodyCore=""
         for i in range(0,len(el)):
              bodyCore+="\"{#%s}\":\"%s\"," %(itLab[i],el[i])
         bodyPost="},\n"
         body+=bodyPre+bodyCore[0:-1]+bodyPost 

    body=body[0:-2]
    print preamble+body+postamble
    return 0
