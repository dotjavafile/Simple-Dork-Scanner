import requests,json,random,time
from bs4 import BeautifulSoup
import threading

bing_search = "http://www.bing.com/search?q="
bing = "http://bing.com"
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
		crawl(self.url)
		#print "Exiting " + self.name


		
def crawl(url):
	global delay,scraped
	url = bing_search+url
	try:
		while True:
			headers = {"User-Agent": random.choice(useragentList)}
			output = requests.get( url , headers=headers)
			bs = BeautifulSoup(output.text.encode('utf-8'), 'html.parser')
			for li in bs.find_all('li', class_='b_algo'):
				ul =  li.a['href']
				if '?' in ul and '=' in ul:
					print ul
					f = open(scraped,'a')
					f.write(ul+'\n')
					f.close()
			url = bing + bs.find('a',class_="sb_pagN")['href']
			time.sleep(delay)
	except:
		pass
		#print 'finished'
		
def doMainCrawl():
	global threads
	dorksList = []
	
	with open(dorks,'a+') as file:
		for line in file:
			dorksList.append(line.rstrip())
	while len(dorksList)>0:
		for num in range (0,20):
			threads.append(myThread(num,"Thread-"+str(num), dorksList[0]))
			dorksList.pop(0)
			if(len(dorksList)<=0):
				break
		for t in threads:
			t.start()
		for t in threads:
			t.join()
		threads = []
	