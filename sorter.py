import operator
import sys
import csv
from Settingsv2 import ROUNDS

# This sorts the file by username, and it remains in time-ascending order within usernames.

def sortbyUsername():
	i = 1
	while i < (ROUNDS + 1):

		reader = csv.reader(open('all' + str(i) + '.csv'), delimiter=',')

		ab2 = sorted(reader, key=operator.itemgetter(2), reverse=False)
			
		with open('sortedall' + str(i) + '.csv', 'ab') as fp:
			ab = csv.writer(fp, delimiter=',');
			for row in ab2:
				ab.writerow(row);
		
		i = i + 1