import sys, argparse,re,json
import bingdork,proxy,dsss,injectibility

isrunning = True
scrapedList = []
injectableList = []
dorksList = []

config = 'config.txt'
scraped = "scraped.txt"
injectable = "injectable.txt"
dorks = "dorks.txt"

configtxt = ''
with open(config, 'r') as content_file:
    configtxt = content_file.read()
config_json = json.loads(configtxt)
	

		
def main():
	scrapedList = []
	injectableList = []
	dorksList = []
	with open(scraped ,'a+') as file:
		for line in file:
			scrapedList.append(line.rstrip())
		
	with open(injectable ,'a+') as file:
		for line in file:
			injectableList.append(line.rstrip())
			
	with open(dorks ,'a+') as file:
		for line in file:
			dorksList.append(line.rstrip())
			
	scrapedList = list(set(scrapedList))
	injectableList = list(set(injectableList))
	dorksList = list(set(dorksList))
	
	f = open(scraped, 'w')
	for item in scrapedList:
		f.write(item+'\n')
	f.close()
	
	f = open(injectable, 'w')
	for item in injectableList:
		f.write(item+'\n')
	f.close()
	
	f = open(dorks, 'w')
	for item in dorksList:
		f.write(item+'\n')
	f.close()


		
	print 'Scanner tool by Dotjavafile/Rootk4jj'
	print "Total scraped: " + str(len(scrapedList))
	print "Total Injectable: " + str(len(injectableList))
	print "Dorks in dorks.txt: " + str(len(dorksList))

	print "Choose your options"
	print "[1] Mass Scan (bing)"
	print "[2] Injectability Test"
	print "[3] Url Scan"
	print "[4] Check proxies"
	print "[q] Quit program"

	option = raw_input('>')

	if option=='1':
		bingdork.doMainCrawl()
		scrapedList=[]
		with open(scraped ,'a+') as file:
			for line in file:
				scrapedList.append(line.rstrip())
		print 'removing duplicates'
		scrapedList = list(set(scrapedList))
		f = open(scraped, 'w')
		for s in scrapedList:
			f.write(s+'\n')
		f.close()
		raw_input('press any key.....')
	elif option =='2':
		print 'Checking injectibility in scraped list'
		injectibility.doMainCrawl()
		raw_input('press any key.....')
	elif option =='3':
		print 'Url scan'
		website = raw_input('Enter url to scan >')
		result = dsss.scan_page(website if website.startswith("http") else "http://%s" % website)
		print "\nscan results: %s vulnerabilities found" % ("possible" if result else "no")
		raw_input('press any key.....')
	elif option =='4':
		print 'Proxy checking'
		proxy.checkProxy()
		raw_input('press any key.....')
	elif option =='q':
		global isrunning
		isrunning = False
		print "Goodbye"
		
while isrunning:
	main()