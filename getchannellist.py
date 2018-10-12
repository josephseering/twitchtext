import string
import csv

# This is important - it reads in the names of channels to be scraped from a csv named engsample.csv. It's called that because it's a sample of english speaking channels.
def getchannellist():
	CHANNELLIST = []
	
	with open('channellist.csv','rU') as csvinput:
		
		reader = csv.reader(csvinput)
		
		for row in reader:
			CHANNELLIST.append(row[0].strip())
	
	return CHANNELLIST