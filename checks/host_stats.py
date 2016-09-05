#!/usr/bin/python

import sys
import re
import subprocess
from xs_discovery import vmsListCreate

#vmRegExp=re.compile('''uuid \( RO\)\s+: ([\w-]+)''')
# vmRegExp=re.compile('''uuid \( RO\)\s+: (.+)\n\s+name-label \( RW\): ([-\w ]+)''')
cmd="/opt/xensource/bin/xe"

# def _vmsListCreate(lis,hostUUID):

#     opt="vm-list resident-on=%s" %(hostUUID)
#     command="%s %s" %(cmd,opt)

#     out=subprocess.check_output(command.split())
#     for match in vmRegExp.finditer(out):
#         vmUUID=match.groups()[0]
#         vmLabel=match.groups()[1]
#         #print "%s %s" %(vmUUID,vmLabel)
#         # discard dom0
#         if vmLabel != "Control domain on host":
#             lis.append(vmUUID)

#     if len(lis) > 0:    
#         return 0
#     else:
#         # empty list or something weird 
#         print command
#         return 4

def getCPU(vmUUID):
    
    opt="vm-param-get uuid=%s param-name=VCPUs-number" %(vmUUID)
    command="%s %s" %(cmd,opt)

    out=subprocess.check_output(command.split())
    vCPUs=int(out)
    #print "%s has %d cpu." %(vmUUID,vCPUs)
    return vCPUs

if __name__=="__main__":

    vmList=list()
    totVCPUs=0
    hostID=sys.argv[1]
    mode=sys.argv[2]
    vmsListCreate(vmList,"vm-list resident-on=%s" %(hostID))
    if mode == "vmNum":
        print "%d" %(len(vmList))
    elif mode == "vCPUs": 
        vmIDs=[el[0] for el in vmList]     
        for vmID in vmIDs:
            totVCPUs+=getCPU(vmID)
        print "%d" %(totVCPUs) 
    else:
       print "Mandatory option missing or unknown, exiting"
       sys.exit(2)
