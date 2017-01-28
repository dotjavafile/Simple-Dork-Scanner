import urllib2, socket
import threading
socket.setdefaulttimeout(8)

proxy = 'proxy.txt'
threads = []
proxys = []
threadLock = threading.Lock()

class myThread (threading.Thread):
	def __init__(self, threadID, name, pip):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.pip = pip
	def run(self):
		global proxys
		#print "Starting " + self.name
		if is_bad_proxy(self.pip):
			print "Bad Proxy:", self.pip
		else:
			print self.pip, " is working"
			add_proxy(self.pip)

		#print "Exiting " + self.name

def add_proxy(pip):
	global proxys
	proxys.append(pip)
		
		
def is_bad_proxy(pip):	
	try:		
		proxy_handler = urllib2.ProxyHandler({'http': pip})		
		opener = urllib2.build_opener(proxy_handler)
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		urllib2.install_opener(opener)		
		req=urllib2.Request('http://www.google.com')  # change the url address here
		sock=urllib2.urlopen(req)
	except urllib2.HTTPError, e:		
		print 'Error code: ', e.code
		return e.code
	except Exception, detail:
		print "ERROR:", detail
		return 1
	return 0


def checkProxy():
	global proxy,threads,proxys
	proxyList = []
	with open(proxy, 'r') as file:
		for line in file:
			proxyList.append(line.rstrip())
	
	while len(proxyList)>0:
		for num in range (0,30):
			threads.append(myThread(num,"Thread-"+str(num), proxyList[0]))
			proxyList.pop(0)
			if(len(proxyList)<=0):
				break
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		threads = []
	
	proxys = list(set(proxys))
	print 'Total proxy : ' + str(len(proxys))
	f = open(proxy,'w')
	for p in proxys:
		f.write(p+'\n')
	f.close()

			