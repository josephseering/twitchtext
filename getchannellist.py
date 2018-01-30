import string
import csv

# This is important - it reads in the names of channels to be scraped from a csv named engsample.csv. It's called that because it's a sample of english speaking channels.
def getchannellist():
	CHANNELLIST = []
	
	with open('engsample.csv','rU') as csvinput:
		
		reader = csv.reader(csvinput)
		
		for row in reader:
			CHANNELLIST.append(row[0].strip())
	
	return CHANNELLIST


# This is an old thing, don't worry about it	
def getbucketdict():
	BUCKETDICT = {}
	
	with open('engsample.csv','rU') as csvinput:
	
		reader = csv.reader(csvinput)
		
		for row in reader:
			BUCKETDICT[row[0].strip()] = row[3].strip()
	
	return BUCKETDICT