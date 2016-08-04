#!/usr/bin/python

import re
import subprocess
import sys
import os
from zab_utils import lld_render

#pvRegExp=re.compile('\s+((/\w+)*)\s+(.+)\s+(.+)\s+(.+)\s+(.+)G\s+(.+)G')
pvRegExp=re.compile('\s\s((/\w+)*)\s+(.+)\s+(.+)\s+(.+)\s+(.+)G\s+(.+)G')

vgRegExp=re.compile('\s([\w-]+)\s+(\w+)\s+(\w+)\s+(.+)\s+(.+)G\s+(.+)G')

def pvListCreate(lis):
    
    cmd="/usr/sbin/pvs"
    opt="--noheadings --units G"
    command="%s %s" %(cmd,opt)
    DEVNULL = open(os.devnull, 'wb')  
    pvsOut=subprocess.check_output(command.split(),stderr=DEVNULL)
    #print pvsOut
    for match in pvRegExp.finditer(pvsOut):
        pvsLabel=match.groups()[0]
        vg=match.groups()[2]
        formt=match.groups()[3]
        pSize=match.groups()[5]
        pFree=match.groups()[6]
        #print "%s-%s %s %s %s" %(pvsLabel,vg,formt,pSize,pFree)
        lis.append((pvsLabel,vg,formt,pSize,pFree))
    
    if len(lis) > 0:    
        return 0
    else:
        # empty list or something weird 
        print command
        return 4

def vgListCreate(lis):

    cmd="/usr/sbin/vgs"
    opt="--noheadings --units G"
    command="%s %s" %(cmd,opt)
    DEVNULL = open(os.devnull, 'wb')
    vgsOut=subprocess.check_output(command.split(),stderr=DEVNULL)
    for match in vgRegExp.finditer(vgsOut):
        vgLabel=match.groups()[0]
        pvNum=match.groups()[1]
        lvNum=match.groups()[2]
        vSize=match.groups()[4]
        vFree=match.groups()[5]
        #print "%s %s %s %s %s" %(vgLabel,pvNum,lvNum,vSize,vFree)
        lis.append((vgLabel,pvNum,lvNum,vSize,vFree))
    
    if len(lis) > 0:    
        return 0
    else:
        # empty list or something weird 
        print command
        return 4    
    


if __name__=="__main__":

    lis=list()
    listFlag=-1
    if sys.argv[1]=="pv":
       listFlag=pvListCreate(lis)
       listLabels=("PVLABEL","VGLABEL","PVFMT","PVSIZE","PVFREE")
    elif sys.argv[1]=="vg":
       listFlag=vgListCreate(lis)
       listLabels=("VGLABEL","PVNUM","LVNUM","VGSIZE","VGFREE")
    else:
       print "Mandatory option missing or unknown, exiting"
       sys.exit(2)

    if listFlag == 0:
        lld_render(lis,listLabels)
    else:
        print "some errors occured executing the above command, please fix it"
        sys.exit(4)
