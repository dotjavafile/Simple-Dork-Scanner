import requests,json,random,time
from bs4 import BeautifulSoup
import threading,dsss

threads = []
delay = 1
timeout = 5
useragentList =  []
useragent = "useragents.txt"

config = 'config.txt'
scraped = "scraped.txt"
injectable = "injectable.txt"
dorks = "dorks.txt"

urls = []

with open(useragent,'r') as file:
	for line in file:
		useragentList.append(line.rstrip())

class myThread (threading.Thread):
	def __init__(self, threadID, name, url):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.url = url
	def run(self):
		global proxys
		#print "Starting " + self.name
		test(self.url)
		#print "Exiting " + self.name


		
def test(url):
	global delay,injectable
	result = dsss.scan_page(url if url.startswith("http") else "http://%s" % url)
	print "\nscan results: %s vulnerabilities found" % ("possible" if result else "no")
	if result:
		f = open(injectable,'a')
		f.write(url+'\n')
		f.close()
		
def doMainCrawl():
	global threads,scraped
	scrapedList = []
	
	with open(scraped,'a+') as file:
		for line in file:
			scrapedList.append(line.rstrip())
	while len(scrapedList)>0:
		for num in range (0,100):
			threads.append(myThread(num,"Thread-"+str(num), scrapedList[0]))
			scrapedList.pop(0)
			if(len(scrapedList)<=0):
				print 'finished'
				break
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		threads = []
	