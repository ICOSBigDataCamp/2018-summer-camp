from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

#read web page directly
url = 'http://www.umich.edu/'
html = urlopen(url).read();
#time.sleep(10)

#create BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

links = []
for linkcd in soup.find_all("a"):
	url = linkcd.get('href')
	print 'L1:',url
	links.append(url)

ct = 0
links2 = []
for link in links:
	try:
		html = urlopen(link).read();
		ct += 1
		print ct,'going to',link
		soup = BeautifulSoup(html, "html.parser")
		for linkcd in soup.find_all("a"):
			url = linkcd.get('href')
			print 'L2:',url
			links2.append(url)
		time.sleep(10)
	except:
		print 'could not load',link
	if ct > 0: break
	