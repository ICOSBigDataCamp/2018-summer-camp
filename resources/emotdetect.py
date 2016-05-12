#calculate pos/neg sentiment scores

import re
	
poswrds = {}
with open("poslist.txt") as f:
	for line in f:
		line = line.strip()
		poswrds[line] = 1
print len(poswrds),'positive words loaded'

negwrds = {}
with open("neglist.txt") as f:
	for line in f:
		line = line.strip()
		negwrds[line] = 1
print len(negwrds),'negative words loaded'
print
		
posct=0; negct=0; totct=0
with open("srctext.txt") as f:
	for line in f:
		#pre-processing to put into lower-case & remove punctuation
		line = line.lower()
		line = re.sub(r'[^\w\s]','',line) #this says replace anything that's not a word-character (\w) or a space character (\s) w/ an empty string
		words = line.split(); totct += len(words)
		for word in words:
			if word in poswrds:
				posct += 1
			if word in negwrds:
				negct += 1

if negct>0:
	posneg = float(posct)/negct
else:
	posneg = 100
posper = float(posct)/totct; negper = float(negct)/totct
print 'results from analysis of source text:'
print totct,'total words found,',posct,'positive &',negct,'negative'
print 'percent positive words:',posper
print 'percent negative words:',negper
print 'ratio of positive to negative:',posneg