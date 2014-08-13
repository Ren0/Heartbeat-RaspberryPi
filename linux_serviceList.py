#i#################
import sys
import subprocess
import csv
import os
# command line : sudo netstat -tlnp | awk '/:[0-9]*/ {split($NF,a,"/"); split($4,b,":"); print b[2],a[1]}'
# and ps x | awk '$1==1918 {n=split($NF,a,"/");n=split(a[n],b,".");print b[1]}'

cmdPortAndPid = "sudo netstat -tlnp | awk '/:[0-9]*/ {split($NF,a,\"/\"); split($4,b,\":\"); print b[2],a[1]}'"
output,error = subprocess.Popen(cmdPortAndPid, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def getStringList():
	stringResult = ''
	for line in output.split(os.linesep):
		result = line.split(' ', 1)		
		if len(result) != 2 :
			continue
		port = result[0]
		pid = result[1]
		service = "not defined"
		if port == "22" :
			service = "ssh"
		else :
			cmdPidToName = "ps x | awk '$1=="+pid+" {n=split($NF,a,\"/\");n=split(a[n],b,\".\");print b[1]}'"
			service,error = subprocess.Popen(cmdPidToName, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()	
			service = service.rstrip('\n')
		print service, ":", port, ";"
		stringResult += service
		stringResult += ":"
		stringResult += port
		stringResult += ";"
	return stringResult

if __name__ == "__main__":
	print getStringList()