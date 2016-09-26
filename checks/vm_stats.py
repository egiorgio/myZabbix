#!/usr/bin/python

# Import the os module, for the os.walk function
import os
import sys
import re 
from datetime import datetime
import subprocess        

def vmBackupCount(baseDir,vmLabel):

    backupRegExp=re.compile('(%s)_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}).+FullBackup\.xva' %(vmLabel))
    backupTS_list=[]

    for dirName, subdirList, fileList in os.walk(baseDir):
        #print('Found directory: %s' % dirName)
        for fname in fileList:
            m=backupRegExp.match(fname)
            if m:
               backup_date=m.group(2)
               backupTS=datetime.strptime(backup_date,'%Y-%m-%d_%H-%M-%S').strftime('%s')
               backupTS_list.append(backupTS)
    return sorted(backupTS_list)

def vmSnapshotCount(vmID):
    
    vmRegExp=re.compile('''uuid \( RO\)\s+: (.+)\n\s+name-label \( RW\): ([-\w ]+)''')
    # retrieve all VM snapshot
    # grab their creation date

    command="xe snapshot-list snapshot-of=%s" %(vmID)
    out=subprocess.check_output(command.split())
    snapDict={}

    for match in vmRegExp.finditer(out):
        snapUUID=match.groups()[0]
        snapLabel=match.groups()[1]
        snapDate=getSnapshotDate(snapUUID)  
        snapDict[snapUUID]=(snapLabel,snapDate)

    return snapDict

def getSnapshotDate(snapUUID):

    command="xe snapshot-param-get uuid=%s param-name=snapshot-time" %(snapUUID)

    out=subprocess.check_output(command.split())
    out=out[:-1]
    snapDate=datetime.strptime(out,'%Y%m%dT%H:%M:%SZ').strftime('%s')
    return snapDate

     
if __name__=="__main__":
    
    if "bkp" in sys.argv[1]:

        rootDir = sys.argv[2]
        vmLabel = sys.argv[3]
        bkp_list=vmBackupCount(rootDir,vmLabel)

        if sys.argv[1] == "bkpcount":
            print len(bkp_list)
        elif sys.argv[1] == "bkplast":
            if len(bkp_list) > 0:
                print bkp_list[-1]
            else:
                print "0000000001"

    elif "snap" in sys.argv[1]:
       snapDict=vmSnapshotCount(sys.argv[2])
       if sys.argv[1] == "snapcount":
         print len(snapDict)
       elif sys.argv[1] == "snaplast":
         lastTS=datetime.strptime("20000101T00:00:01Z",'%Y%m%dT%H:%M:%SZ').strftime('%s')
         for uuid in snapDict:
             if int(snapDict[uuid][1]) > int(lastTS):
                 lastTS=snapDict[uuid][1]
         print lastTS
    else:
         pass
        
