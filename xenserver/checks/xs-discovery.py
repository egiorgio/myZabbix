#!/usr/bin/python

import sys
import re
import subprocess
from zab_utils import lld_render

hsRegExp=re.compile('''uuid \( RO\)\s+: (.+)\n\s+name-label \( RW\): ([\w-]+)''')
#srRegExp=re.compile('''uuid \( RO\)\s+:(.+)\n\s+name-label \( RW\): ([\w-]+).+type \( RO\): ([\w-]+)''')
# skips two lines, between name-label and type
srRegExp=re.compile('''uuid \( RO\)\s+: (.+)\n\s+name-label \( RW\): ([\s\w-]+)\n(.+\n){2}\s+type \( RO\): ([\w-]+)''')

def hostListCreate(lis):

    cmd="/opt/xensource/bin/xe"
    opt="host-list"
    command="%s %s" %(cmd,opt)

    out=subprocess.check_output(command.split())
    for match in hsRegExp.finditer(out):
        hostUUID=match.groups()[0]
        hostLabel=match.groups()[1]
        #print "%s %s" %(hostUUID,hostLabel)
        lis.append((hostUUID,hostLabel))

    if len(lis) > 0:    
        return 0
    else:
        # empty list or something weird 
        print command
        return 4

def srListCreate(lis):

    cmd="/opt/xensource/bin/xe"
    opt="sr-list"
    command="%s %s" %(cmd,opt)

    out=subprocess.check_output(command.split())
    for match in srRegExp.finditer(out):
        srUUID=match.groups()[0]
        srLabel=match.groups()[1]
        srType=match.groups()[3] 
        #print "%s %s" %(hostUUID,hostLabel)
        lis.append((srUUID,srLabel,srType))

    if len(lis) > 0:    
        return 0
    else:
        # empty list or something weird 
        print command
        return 4

if __name__=="__main__":

    lis=list()
    listFlag=-1
    if sys.argv[1]=="host":
       listFlag=hostListCreate(lis)
       listLabels=("HOSTUUID","HOSTLABEL")
    elif sys.argv[1]=="sr":
       listFlag=srListCreate(lis)
       listLabels=("SRUUID","SRLABEL","SRTYPE")
    else:
       print "Mandatory option missing or unknown, exiting"
       sys.exit(2)

    if listFlag == 0:
        lld_render(lis,listLabels)
    else:
        print "some errors occured executing the above command, please fix it"
        sys.exit(4)
