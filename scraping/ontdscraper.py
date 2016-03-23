from bs4 import BeautifulSoup
from urllib2 import urlopen
import time
import sqlite3

# create db, open link to db, and create table
try:
	conn = sqlite3.connect('ontd.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE articles
             (id integer, title text, labels text, commct text, commurl text)''')
except:
	c = conn.cursor()

#read text source file
#f = open('ontdsrc.txt', 'r')
#html = f.read()

#read web page directly
url = 'http://ohnotheydidnt.livejournal.com/'
html = urlopen(url).read();
#time.sleep(10)

#create BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

print '\nCollecting articles...'
artct=0
for art in soup.find_all('article'):
	artct+=1; title,labels,commurl,commct = '',[],'',''
	for tag in art.descendants:
		#print(tag)
		try:
			if tag['class'][0] == 'j-e-title':
				#print artct,':',tag.a.string
				title = tag.a.string
				title = title.encode('ascii', 'ignore')
		except:
			pass
		try:
			if tag['class'][0] == 'j-e-tags-item':
				#print artct,':',tag.a.string
				labels.append(tag.a.string)
		except:
			pass
		try:
			if tag['class'][1] == 'j-e-nav-item-comments':
				#print artct,':',tag.a.string
				commct = tag.a.string
				#print artct,':',commurl
				commurl = tag.a.get('href')
		except:
			pass	
	print artct,title,labels,commct,commurl
	# Insert a row of data
	#c.execute("INSERT INTO articles(id, title, labels, commct, commurl) VALUES (artct,title,labels,commct,commurl)")
	labstr = '; '.join(labels)
	rec = [artct,title,labstr,commct,commurl]
	c.execute("INSERT INTO articles VALUES (?,?,?,?,?)",rec)
	# Save (commit) the changes
	conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
print '\narticles found: ',artct