#!/usr/bin/python

import sys, urllib, urllib2, socket, getopt

# crontab example: 30 * * * * python /home/pi/administration/heartbeat.py
def main(argv):
	targetServer = 'http://127.0.0.1/'
	machinename = 'myRaspberryPi'
	location = 'London'
	headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
	ipProviderUrl = 'http://ip.42.pl/raw'

	# Service list managment
	runningServiceRetrieverPath = "/home/pi/administration/linux_serviceList.py"
	serviceList = "notSet"
	if os.path.isfile(runningServiceRetrieverPath) :
		proc = subprocess.Popen(['python', runningServiceRetrieverPath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		serviceList = proc.communicate()[0]
		
	try:
		opts, args = getopt.getopt(argv,'ht:m:l:')
		if(len(opts) < 2):
			exit()
	except getopt.GetoptError:
		exit()

	for opt, arg in opts:
		if opt == '-h':
			exit()
		elif opt in ('-t'):
			targetServer = arg
		elif opt in ('-m'):
			machinename = arg
		elif opt in ('-l'):
			location = arg
		else:
			exit()
			
	hostname = socket.gethostname()
	url = urllib2.urlopen(ipProviderUrl).read()
	
	params = urllib.urlencode({'hostname': hostname, 'machinename': machinename, 'location': location, 'url': url, 'serviceList': serviceList})
	f = urllib.urlopen(targetServer, params)

def exit():
	print 'Usage\t: heartbeat.py -t <targetServer> -m <machinename> -l <location>\nExample\t: heartbeat.py -t myTargetServer -m myRaspberryPi -l London'
	sys.exit(2)
	
if __name__ == '__main__':
	main(sys.argv[1:])