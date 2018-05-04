#practice collecting data from imdb

#import some handy packages
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time
import random
import re
import csv

#setup two output files (fbak for storing websites collected, fout for storing data scraped)
fbak = open('src-pgs.txt', 'wb')
fout = open('imdb-recs.txt', 'wb')
#create a handle to write tab-delimited data to the file fout
writer = csv.writer(fout, delimiter='\t')
#send the header row to this handle
writer.writerow(['movie','position','actor','actor_url','role','role_url'])

#read in html from text or website (only 1 of next 2 lines should be active)
f = open('imdb-src.txt', 'rb'); html = f.read()
#html = urlopen('http://www.imdb.com/title/tt2488496/?ref_=nv_sr_1').read(); fbak.write(html); time.sleep(random.randint(4, 10));
#note: the previous line loads the html from the url, stores it in our backup file, and then sleeps for a random # of seconds b/w 4 & 10
#  sleeping is essential to avoid annoying web servers by calling them too often!

#convert the html into a format that recognizes the structure of the html (and put it into a variable we're calling soup)
soup = BeautifulSoup(html, "html.parser")

#this snippet prints all the links on the page
for link in soup.find_all('a'):
    print(link.get('href'))
	
#and this one prints all the text (note the encoding method is used to avoid errors from unicode characters)
txt = soup.get_text(); txt = txt.encode('ascii', 'ignore'); print txt



#***Code below finds all the variables we want about actors and outputs them to fout***

#get movie title, which is string stored under html 'title' tag, & strip out any whitespace at the start/end
movie = soup.title.string.strip()
#find the 'cast' table
table = soup.find("table", class_="cast_list")
#find all the rows from the table and create a row-counter
rows = table.find_all("tr"); rowct=0
#iterate thru rows
for row in rows:
	#find all the columns in the row
	cols = row.find_all("td")
	#skip this row if it doesn't contain more than one column
	if not (len(cols)>1): continue
	#create a list to hold our data
	rec = []
	#add movie title to our list
	rec.append(movie)
	#increment row-counter and store counter at end of our list (this is actor position in the billing)
	rowct+=1; rec.append(rowct)
	#iterate thru columns
	for col in cols:
		#get the text stored under the row-column and strip out any whitespace at the start/end
		txt = col.text.strip()
		#proceed if text contains alphanumeric values (note: uses regex package called re)
		if re.search('[a-zA-Z0-9]', txt):
			#add the text to the end of our list
			rec.append(txt)
			#get link associated w/ actor/role & add to the end of our list (find html 'a' tag, then find value stored under 'href' in this tag)
			link = col.find("a"); url = link["href"]; rec.append(url)
	#send our list to the output handle
	writer.writerow(rec)
#report how many good rows were found
print 'parsed',movie
print 'actors found:',rowct